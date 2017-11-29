import pprint

from modules.lepd.LepDClient import LepDClient

__author__ = 'Mac Xu <mac.xxn@outlook.com>'


class PerfProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config
        
        self.dataCount = 25


    def parse_perf_block(self, block_lines):
        first_line = block_lines.pop(0)
        # first line is like this:
        # swapper     0 [000] 1212828.569239:   10101010 cpu-clock:
        header_line_entities = first_line.split()

        perf_block = {
            'process': header_line_entities[0],
            'pid': header_line_entities[1],
            'CCC': header_line_entities[2],
            'DDD': header_line_entities[3],
            'EEE': header_line_entities[4],
            'FFF': header_line_entities[5],

            'children': []
        }

        for child_line in block_lines:
            child_entities = child_line.split()
            perf_block['children'].append({
                'address': child_entities[0],
                'process_name': child_entities[1],
                'symbol': child_entities[2]
            })

        return perf_block

    def get_cmd_perf_flame(self, response_lines=None):

        lepd_command = 'GetCmdPerfFlame'

        if not response_lines:
            response_lines = self.client.getResponse(lepd_command)
        elif isinstance(response_lines, str):
            response_lines = self.client.split_to_lines(response_lines)

        if len(response_lines) == 0:
            return {}

        # for line in response_lines:
        #     print(line)

        parsed_blocks = []

        block_lines = []
        for line in response_lines:
            # each block is separated by an empty line
            if line.strip():
                block_lines.append(line)
                continue

            parsed_block = self.parse_perf_block(block_lines)
            parsed_blocks.append(parsed_block)
            block_lines = []

        return parsed_blocks

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
        while not response_lines[0].startswith(column_header_line_prefix):
            response_lines.pop(0)
        
        response_lines.pop(0)
        response_lines.pop(0)
        response_lines.pop(0)

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


if __name__ == '__main__' :
    profiler = PerfProfiler(server='www.rmlink.cn', config='debug')

    pp = pprint.PrettyPrinter(indent=2)

    responseData = profiler.get_cmd_perf_flame()
    pp.pprint(responseData)

