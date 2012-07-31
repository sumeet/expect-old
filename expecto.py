from functools import partial


class ExpectationError(Exception):
    pass


def new_expecto(**kwargs):
    return lambda expect_args: Expecto(expect_args, **kwargs)


class Expecto:

    def __init__(self, expect_args, **methods):
        for name, method in methods.iteritems():
            vars(self)[name] = partial(method, expect_args)

    def stub(self, arg_name):
        return
