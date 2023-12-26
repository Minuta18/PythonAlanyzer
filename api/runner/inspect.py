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
        
    def _modify_file(self, tabsize: int = 4):
        with open(self.filename, 'r+') as f:
            text = f.readlines()
        with open(self.filename, 'w') as f:
            for ind, line in enumerate(text):
                line.replace('\t', ' ' * tabsize)
                f.write(f'{" " * self._get_spaces(line)}print({ind}, ":", locals())\n')
                f.write(line)

    async def inspect(self) -> dict:
        self._modify_file(tabsize=self.tabsize)
        sbox = sandbox.NoSandBox(self.filename, timeout=TIME_LIMIT)
        out, _ = await sbox.get_output()
        out = out.decode('utf-8')
        out_dict = {}

        for line in out.split('\n'):
            dots_ind = line.find(':')
            if dots_ind != -1:
                try:
                    out_dict[int(line[:dots_ind - 1])] = eval(line[dots_ind + 2:].replace('<', '"').replace('>', '"'))
                except SyntaxError:
                    out_dict[int(line[:dots_ind - 1])] = line[dots_ind + 2:]

        return out_dict

if __name__ == '__main__':
    ins = Inspector('test.py', 4)
    ins.inspect()
