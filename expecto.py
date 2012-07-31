from functools import partial


class ExpectationError(Exception):
    pass


def new_expecto(**methods):
    return lambda arg: Expecto(arg, **methods)


class Expecto:

    def __init__(self, arg_expect_called_with, **methods):
        self._arg_expect_called_with = arg_expect_called_with
        self._set_methods(methods, arg_expect_called_with)

    def stub(self, arg_name):
        def _(*args):
            raise ExpectationError
        self._arg_expect_called_with.classmethod = staticmethod(_)
        return self

    def with_(self, *args, **kwargs):
        return

    def _set_methods(self, methods, arg_expect_called_with):
        for name, method in methods.iteritems():
            vars(self)[name] = partial(method, arg_expect_called_with)
