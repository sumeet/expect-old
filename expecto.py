from functools import partial


class ExpectationError(Exception):
    pass


def new_expecto(**methods):
    return lambda arg: Expecto(arg, **methods)


class Expecto:

    def __init__(self, arg, **methods):
        self._arg = arg
        for name, method in methods.iteritems():
            vars(self)[name] = partial(method, arg)

    def stub(self, arg_name):
        def _(*args):
            raise ExpectationError
        self._arg.classmethod = staticmethod(_)
        return self

    def with_(self, *args, **kwargs):
        return
