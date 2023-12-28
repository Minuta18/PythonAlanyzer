import subprocess
import os

PYTHON_INTERPRETER = 'python3'

class ISandBox:
    def __init__(self, filename: str, timeout: int = 15): raise NotImplementedError
    def get_output(self) -> (bytes, bytes): raise NotImplementedError

class NoSandBox(ISandBox):
    def __init__(self, filename: str, timeout: int = 15):
        self.filename = filename
        self.proc = subprocess.Popen(
            self._get_command(),
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.timeout = timeout

    def __del__(self):
        # os.remove(self.filename)
        pass

    def _get_command(self):
        return [PYTHON_INTERPRETER, self.filename]

    async def get_output(self):
        try:
            out, err = self.proc.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            out, err = self.proc.communicate(timeout=self.timeout)
        return out, err, self.proc.returncode
