import pprint

from app.modules.lepd.LepDClient import LepDClient
from app.modules.profilers.perf.flameBurner import FlameBurner

__author__ = 'Mac Xu <mac.xxn@outlook.com>'
__author__ = 'Ran Meng <1329597253@qq.com>'


class PerfProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config
        self.flame_burner = FlameBurner()
        
        self.dataCount = 25

    def get_perf_cpu_clock(self, response_lines=None):

        lepd_command = 'GetCmdPerfCpuclock'

        if not response_lines:
            response_lines = self.client.getResponse(lepd_command)
        elif isinstance(response_lines, str):
            response_lines = self.client.split_to_lines(response_lines)

        if len(response_lines) == 0:
            return {}

        response_data = {}
        if self.config == 'debug':
            response_data['rawResult'] = response_lines[:]
            response_data['lepd_command'] = lepd_command

        column_header_line_prefix = '# Overhead'
        
        try:
            while not response_lines[0].startswith(column_header_line_prefix):
                response_lines.pop(0)
            response_lines.pop(0)
            response_lines.pop(0)
            response_lines.pop(0)
        except Exception as e:
            print(response_lines," ----------- GetCmdPerfCpuclock")
            return {}

        result_list = []
        for line in response_lines:
            if line.strip() == '':
                continue

            line_values = line.split()

            if len(line_values) < 5:
                # print('                     --------------- skip it.')
                continue

            if '%' not in line_values[0]:
                # print('                     --------------- skip it.')
                continue

            result_line = {}
            result_line['Overhead'] = line_values[0]
            result_line["Command"] = line_values[1]
            result_line["Shared Object"] = line_values[2]
            result_line['Symbol'] = ' '.join([str(x) for x in line_values[3:]])

            result_list.append(result_line)
            if len(result_list) >= self.dataCount:
                # print('now the length of the array is greater than the max, break here')
                break

        response_data['data'] = result_list

        return response_data

    def get_cmd_perf_flame(self, response_lines=None):

        lepd_command = 'GetCmdPerfFlame'

        if not response_lines:
            response_lines = self.client.getResponse(lepd_command)
        elif isinstance(response_lines, str):
            response_lines = self.client.split_to_lines(response_lines)

        if len(response_lines) == 0:
            return {}

        flame_data = self.flame_burner.burn(response_lines)
        flame_data_hierarchy = []
        # self.flame_burner.generate_json_hierarchy(flame_data, [], flame_data_hierarchy)

        return {'flame': flame_data, 'perf_script_output': response_lines, 'hierarchy': flame_data_hierarchy}


if __name__ == '__main__' :
    profiler = PerfProfiler(server='www.rmlink.cn', config='debug')

    pp = pprint.PrettyPrinter(indent=2)

    responseData = profiler.get_cmd_perf_flame()
    # pp.pprint(responseData)

