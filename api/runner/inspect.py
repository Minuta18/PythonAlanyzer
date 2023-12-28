from runner import sandbox

TIME_LIMIT = 10

class Inspector:
    def __init__(self, filename: str, tabsize: int = 4):
        self.filename = filename
        self.tabsize = tabsize
        
    def _get_spaces(self, line: str):
        space_cnt = 0
        for char in line:
            if char != ' ':
                break
            else:
                space_cnt += 1
        return space_cnt
    
    def _modify_line(self, line: str, next_line: str, print_payload: str):
        new_line = ' ' * max(self._get_spaces(line), self._get_spaces(next_line))
        new_line += f'print("{print_payload}", locals(), '
        new_line += "' '.join([str(i) for i in map(type, locals().values())]), sep='\\n', file=sys.stderr)\n"
        return new_line

    def _modify_file(self, tabsize: int = 4):
        with open(self.filename, 'r+') as f:
            text = f.readlines()
        with open(self.filename, 'w') as f:
            f.write('import sys\n')
            for ind, line in enumerate(text[:-1]):
                line.replace('\t', ' ' * tabsize)
                f.write(line)
                f.write(self._modify_line(text[ind], text[ind + 1], f'{ind + 1}:'))
            f.write(text[-1].replace('\t', ' ' * tabsize) + '\n')
            f.write(self._modify_line(text[-1], '', f'{len(text)}:'))

    def _parse_out(self, out: str) -> (dict, str):
        out_dict = dict()
        lines = out.split('\n')
        err = ''

        i = 0
        while i < len(lines) - 1:
            i += 1
            if lines[i].startswith('Traceback'):
                err = '\n'.join(lines[i:])
            try:
                line_ind = int(lines[i][:-1])
            except ValueError:
                continue
            if lines[i][:-1]:    
                out_dict[line_ind] = {'values': ..., 'types': ...}
                out_dict[line_ind]['values'] = eval(
                    lines[i + 1].replace('<', '"').replace('>', '"')
                )

                out_dict[line_ind]['types'] = lines[i + 2].split("'> <class '")
                if len(out_dict[line_ind]['types']) > 0:
                    out_dict[line_ind]['types'][0] = out_dict[line_ind]['types'][0].removeprefix("<class '")
                    out_dict[line_ind]['types'][-1] = out_dict[line_ind]['types'][-1].removesuffix("'>")
        
        typed_out_dict = dict()
        for key, _ in out_dict.items():
            typed_dict = dict()
            keys = list(out_dict[key]['values'].keys())
            for ind in range(len(keys)):
                typed_dict[keys[ind]] = {
                    'value': out_dict[key]['values'][keys[ind]],
                    'type': out_dict[key]['types'][ind],
                }
            typed_out_dict[key] = typed_dict

        return typed_out_dict, err

    async def inspect(self) -> (dict, dict):
        self._modify_file(tabsize=self.tabsize)
        sbox = sandbox.NoSandBox(self.filename, timeout=TIME_LIMIT)
        out, err, code = await sbox.get_output()
        out = out.decode('utf-8')
        err = err.decode('utf-8')

        out_dict, error = self._parse_out(err)
        return out_dict, {'out': out, 'err': error, 'code': code}

if __name__ == '__main__':
    ins = Inspector('test.py', 4)
    ins.inspect()
