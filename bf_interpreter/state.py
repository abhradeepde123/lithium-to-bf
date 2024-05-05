import logging
import msvcrt


class BFState:
    UNFINISHED = 0
    FINISHED = 1

    def __init__(
            self,
            errors,
            text: str,
            mem_length: int,
            fn: str = "<stdin>",
            logger: logging.Logger = logging.getLogger(__name__)
    ):
        self.text = text
        self.mem_length = mem_length
        self.fn = fn
        self.logger = logger
        self.errors = errors

        self.memory = [0 for _ in range(mem_length)]
        self.mem_value = 0

        self.ptr = -1
        self.mem_ptr = 0

        self.inst = ""
        self.brace_map = []
        self.error = None

    def advance_char(self):
        if self.ptr < -1:
            self.error = self.errors.BFSyntaxError(self.ptr, self.text, self.fn, "no start for this loop")
        elif self.mem_ptr < 0 or self.mem_ptr > self.mem_length:
            self.error = self.errors.BFStackOverflowError(
                self.ptr, self.text, self.fn,
                f"invalid memory location {self.mem_ptr}"
            )
        if self.error:
            for line in self.error.as_string():
                self.logger.error(line)
            return BFState.FINISHED
        self.ptr += 1

        self.mem_value = self.memory[self.mem_ptr]
        try:
            self.inst = self.text[self.ptr]
        except IndexError:
            return BFState.FINISHED
        return BFState.UNFINISHED

    def do_next_inst(self):
        if res := self.advance_char():
            yield res

        INST_MAP = {
            ".": lambda: print(chr(self.mem_value), end=""),
            ",": lambda: self.memory.__setitem__(self.mem_ptr, ord(msvcrt.getch())),
            "+": lambda: self.memory.__setitem__(self.mem_ptr, (self.mem_value + 1) % 256),
            "-": lambda: self.memory.__setitem__(self.mem_ptr, (self.mem_value - 1) + (256 * (0 > self.mem_value - 1))),
            ">": lambda: self.__setattr__("mem_ptr", self.mem_ptr + 1),
            "<": lambda: self.__setattr__("mem_ptr", self.mem_ptr - 1),
            "[": lambda: self.brace_map.append(self.ptr),
            "]": lambda: (self.mem_value == 0 and self.brace_map.pop())
                         or (self.mem_value != 0 and not self.__setattr__("ptr", self.brace_map[-1]))
        }

        if self.inst in ".,+-><[]":
            INST_MAP[self.inst]()
        yield res
