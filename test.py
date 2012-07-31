import unittest

from expecter import expect
from mock import Mock

from expecto import ExpectationError
from expecto import new_expecto


class ExpectoTest(unittest.TestCase):

    def test_delegates_to_eq(self):
        assert_equal = Mock(name='assert_equal')
        expecto = new_expecto(__eq__=assert_equal)
        expecto('a') == 'b'
        assert_equal.assert_called_once_with('a', 'b')

    def test_stub_with_wrong_argument_raises_exception(self):
        class MyClass(object): pass
        expecto = new_expecto()
        expecto(MyClass).stub('classmethod').with_(1)
        with expect.raises(ExpectationError):
            MyClass.classmethod(2)
