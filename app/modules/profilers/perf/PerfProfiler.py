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

        call_stacks = []

        first_line = block_lines.pop(0)
        # first line is like this:
        # swapper     0 [000] 1212828.569239:   10101010 cpu-clock:
        header_line_entities = first_line.split()
        call_stacks.append(header_line_entities[0])

        # the rest lines look like this:
        # 7fff810665d6 native_safe_halt ([kernel.kallsyms])
        # 7fff8103ae1e default_idle ([kernel.kallsyms])
        for child_line in block_lines:
            child_entities = child_line.split()
            call_stacks.append((child_entities[1]))

        return call_stacks

    def get_cmd_perf_flame(self, response_lines=None):

        lepd_command = 'GetCmdPerfFlame'

        if not response_lines:
            response_lines = self.client.getResponse(lepd_command)
        elif isinstance(response_lines, str):
            response_lines = self.client.split_to_lines(response_lines)

        if len(response_lines) == 0:
            return {}

        for line in response_lines:
            print(line)

        flame_data = {}

        flame_call_stacks = []
        block_lines = []
        for line in response_lines:
            # each block is separated by an empty line
            if line.strip():
                block_lines.append(line)
                continue

            parsed_block = self.parse_perf_block(block_lines)
            flame_call_stacks.append(parsed_block)
            block_lines = []

        flame_chart_data = self.build_flame_data(flame_call_stacks)

        return flame_chart_data


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

        response_data['data'] = {}
        response_data['data']['detail'] = result_list
        response_data['data']['flame'] = self.build_flame_data(result_list)

        return response_data

    def build_flame_data(self, call_stacks):

        flame_data = {}

        active_flame_node = flame_data
        for call_stack in call_stacks:
            print(call_stack)

            while len(call_stack) > 0:
                item_name = call_stack.pop()
                print(item_name)

                if item_name not in active_flame_node:
                    active_flame_node[item_name] = {
                        'name': item_name,
                        'value': 1,
                        'children': []
                    }
                else:
                    active_flame_node[item_name]['value'] += 1

                active_flame_node = active_flame_node[item_name]

        return flame_data




if __name__ == '__main__' :
    profiler = PerfProfiler(server='www.rmlink.cn', config='debug')

    pp = pprint.PrettyPrinter(indent=2)

    responseData = profiler.get_cmd_perf_flame()
    pp.pprint(responseData)

