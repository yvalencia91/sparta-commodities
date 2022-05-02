from builtins import Exception


class GeneralErrorForExtensions(Exception):
    def __str__(self):
        return "This error might not be use for this example"
