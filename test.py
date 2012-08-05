import unittest

from expecter import expect
from mock import Mock

from expecto import new_expecto


class ExpectoTest(unittest.TestCase):

    class MyClass(object):
        @classmethod
        def classmethod(cls): pass

    def setUp(self):
        self.expecto = new_expecto()

    def test_delegates_to_eq(self):
        assert_equal = Mock(name='assert_equal')
        expecto = new_expecto(__eq__=assert_equal)
        expecto('a') == 'b'
        assert_equal.assert_called_once_with('a', 'b')

    def test_stub_with_wrong_argument_raises_exception(self):
        self.expecto(self.MyClass).stub('classmethod').with_(1)
        self.MyClass.classmethod(2)
        with expect.raises(AssertionError):
            self.expecto.verify()

    def test_stub_returns_argument(self):
        self.expecto(self.MyClass).stub('classmethod').with_(1).and_return(2)
        expect(self.MyClass.classmethod(1)) == 2

    def test_stub_does_not_raise_exception_if_not_called(self):
        self.expecto(self.MyClass).stub('classmethod').with_(1).and_return(2)
        self.expecto.verify()

    def test_mock_expectation_raises_exception_if_not_called(self):
        (self.expecto(self.MyClass).should_receive('classmethod').with_(1)
                                   .and_return(2))
        with expect.raises(AssertionError):
            self.expecto.verify()


if __name__ == '__main__':
    unittest.main()
