from collections import namedtuple
from functools import partial

from mock import patch


def new_expect(**methods):
    return Expect(**methods)


Args = namedtuple('Args', 'args kwargs')


# XXX: Only old style classes can delegate magic methods with __getattr__.
class Expect:

    def __init__(self, **methods):
        self._methods = methods

    def __call__(self, argument):
        self._argument = argument
        return self

    def stub(self, arg_name):
        self._expectation = new_stub_expectation(self._argument, arg_name)

    def should_receive(self, arg_name):
        self._expectation = new_mock_expectation(self._argument, arg_name)
        return self

    def with_(self, *args, **kwargs):
        self._expectation.set_args(*args, **kwargs)
        return self

    def and_return(self, return_value):
        self._expectation.set_return_value(return_value)

    def verify(self):
        self._expectation.verify()

    def reset(self):
        self._expectation.reset()

    def __getattr__(self, name):
        return partial(self._methods[name], self._argument)

    def __repr__(self):
        return ('expect(%r)' % self._argument if self._argument is not
                self._no_argument else 'expect')

    class _no_argument(object): pass
    _argument = _no_argument


class Expectation(object):

    def __init__(self, obj, name, verifier):
        self._patcher = patch.object(obj, name)
        self._stub = self._patcher.start()
        self._verifier = verifier

    def set_return_value(self, value):
        self._stub.return_value = value

    def set_args(self, *args, **kwargs):
        self._with_args = Args(args, kwargs)

    def assert_called_once_with_args(self):
        self._stub.assert_called_once_with(*self._with_args.args,
                                           **self._with_args.kwargs)

    def verify(self):
        self._verifier.verify(self)

    @property
    def was_called(self):
        return self._stub.called

    def reset(self):
        self._patcher.stop()


class VerifiesStubs(object):

    @classmethod
    def verify(cls, stub):
        if stub.was_called:
            stub.assert_called_once_with_args()


class VerifiesMocks(object):

    @classmethod
    def verify(cls, stub):
        stub.assert_called_once_with_args()


new_stub_expectation = lambda obj, name: Expectation(obj, name, VerifiesStubs)
new_mock_expectation = lambda obj, name: Expectation(obj, name, VerifiesMocks)