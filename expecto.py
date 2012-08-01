from functools import partial


class ExpectationError(Exception):
    pass


def new_expecto(**methods):
    return lambda arg: Expecto(arg, **methods)


class Expecto:

    def __init__(self, argument, **methods):
        self._argument = argument
        self._set_methods(methods)

    def stub(self, arg_name):
        def _(*args):
            raise ExpectationError
        self._argument.classmethod = staticmethod(_)
        return self

    def with_(self, *args, **kwargs):
        return

    def _set_methods(self, methods):
        for name, method in methods.iteritems():
            vars(self)[name] = partial(method, self._argument)
