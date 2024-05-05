import argparse
import time

from bf_interpreter.state import *
from bf_interpreter import errors

logger = logging.getLogger(__name__)


class BFArgumentParser:
    DESCRIPTION_MSG = "A Brainfuck interpreter written in pure Python"

    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            description=BFArgumentParser.DESCRIPTION_MSG
        )

        self.arg_parser.add_argument("-f", "--file", help="specify file name to run", default="")
        self.arg_parser.add_argument("-m", "--mem-size", help="specify the maximum memory size", type=int,
                                     default=30000)
        self.arg_parser.add_argument("-v", "--verbose",
                                     help="add verbose output (-vv for max verbosity)", action="count", default=False
                                     )

        self.arg_parser.add_argument("filename", help="file name to run", nargs="?", default="")

        self.args = self.arg_parser.parse_args()

    def get_fn(self):
        if fn := self.args.file or self.args.filename:
            return fn
        logger.error("no file passed into program")
        self.arg_parser.error("unspecified file to run")

    def get_mem_size(self):
        if (mem_size := self.args.mem_size) > 0:
            return mem_size
        raise ValueError("invalid maximum memory size given")

    def get_verbosity(self):
        return self.args.verbose


if __name__ == "__main__":
    try:
        arg_parser = BFArgumentParser()

        filename = arg_parser.get_fn()
        mem_len = arg_parser.get_mem_size()
        verbosity = arg_parser.get_verbosity()

        with open(filename) as f:
            text = f.read()

        state = BFState(errors, text, mem_len, filename, logger)

        start = time.time()
        end = start

        while next(state.do_next_inst()) != BFState.FINISHED:
            end = time.time()

        if verbosity >= 1:
            print()
            print("=" * 20)
            print(f"time: {end - start:.5f}s")
            if verbosity >= 2:
                print(f"memory: {state.memory}")
                if verbosity >= 3:
                    print(f"memory location: {state.mem_ptr + 1}")
    except KeyboardInterrupt:
        exit()
