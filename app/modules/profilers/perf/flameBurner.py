__author__ = 'Ran Meng <1329597253@qq.com>'


class FlameBurner():
    def __init__(self):
        self.__perf_script_lines = []

    def burn(self, perf_script_lines, output_file=''):

        self.__perf_script_lines = perf_script_lines

        list_for_flame = []
        json_for_flame = {"name": "root", "value": 0, "children": []}

        # get list_for_flame
        try:
            list = []
            for line in self.__perf_script_lines:
                # print(line)

                if not line.strip():
                    continue

                if not line.isspace() and line:
                    if not line[0].isspace():
                        list_for_flame.append(list)
                        list = []
                        line = line.strip()
                        list.append(line.split()[0].replace(';',':'))
                    elif line.split()[1] == '[unknown]':
                        list.append(line.split()[2].replace(';',':'))
                    else:
                        list.append(line.split()[1].replace(';',':'))
            list_for_flame[0] = list

            # get json_for_flame
            json_for_flame["value"] = len(list_for_flame)
            for li in list_for_flame:
                li.append(li[0])
                li.pop(0)
                li.reverse()
                self.__create_json(li, json_for_flame["children"])

            if output_file:
                with open(output_file, 'w') as f:
                    f.write(json_for_flame)

            return json_for_flame
        except Exception as err:
            print(err)
            return {}

    def __create_json(self, line, children_list):
        if not line:
            return

        flags = 0
        for i in range(len(children_list)):
            if line[0] == children_list[i]["name"]:
                flags += 1
                children_list[i]["value"] += 1
                self.__create_json(line[1:], children_list[i]["children"])
                break
        if flags == 0:
            dict = {"name": line[0], "value": 1, "children": []}
            children_list.append(dict)
            self.__create_json(line[1:], children_list[-1]["children"])
