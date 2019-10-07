import json
import os
from filelock import FileLock


class Config:
    def __init__(self, json_name, lock=True, lock_timeout=-1):
        if lock:
            self.lock = FileLock(json_name + ".lock", timeout=lock_timeout)
            self.lock.acquire()
        self.json_name = json_name
        if os.path.isfile(json_name):
            self.obj = json.load(open(self.json_name, 'rt'))
        else:
            self.obj = dict()
            self.save()

    def __del__(self):
        if self.lock:
            self.lock.release()

    def __contains__(self, item):
        return item in self.obj

    def __getitem__(self, key):
        return self.obj[key]

    def __setitem__(self, key, value):
        self.obj[key] = value

    def __delitem__(self, key):
        if key in self.obj:
            del self.obj[key]

    def __iter__(self):
        return self.obj.__iter__()

    def save(self):
        json.dump(self.obj, open(self.json_name, 'w'))

    def tree(self):

        syms = (chr(0x2502), chr(0x251C), chr(0x2514), u' ')

        def print_param(param):
            lines = list()
            nodes = 0
            if isinstance(param, dict):
                for param2 in param:
                    nodes += 1
                    lines.append(param2)
                    lines_param, nodes_param = print_param(param[param2])
                    last_num = len(lines_param) - 1
                    for num, line in enumerate(lines_param):
                        if line[0] not in syms:
                            nodes_param -= 1
                            sym = syms[2] if num == last_num or nodes_param == 0 else \
                                syms[1]
                        else:
                            sym = syms[0] if nodes_param > 0 else ' '
                        lines.append(sym + ' ' + line)
            else:
                lines.append(str(param))
                nodes = 1
            return lines, nodes

        lines, nodes = print_param({self.json_name: self.obj})
        res = ""
        for line in lines:
            res += line + '\n'
        return res
