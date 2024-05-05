class BFError:
    def __init__(self, idx, text, fn, message):
        self.idx = idx
        self.text = text
        self.fn = fn
        self.message = message

        self.name = "BFError"
        self.line = self.text.count("\n", 0, self.idx) + 1

    def as_string(self):
        return [
            f"File {self.fn}, line {self.line}, idx {self.idx + 1}",
            f"{self.name}: {self.message}"
        ]


class BFSyntaxError(BFError):
    def __init__(self, idx, text, fn, message):
        super(BFSyntaxError, self).__init__(idx, text, fn, message)
        self.name = "BFSyntaxError"


class BFRecursionError(BFError):
    def __init__(self, idx, text, fn, message):
        super(BFRecursionError, self).__init__(idx, text, fn, message)
        self.name = "BFRecursionError"


class BFStackOverflowError(BFError):
    def __init__(self, idx, text, fn, message="memory limit exceeded"):
        super(BFStackOverflowError, self).__init__(idx, text, fn, message)
        self.name = "BFStackOverflowError"
