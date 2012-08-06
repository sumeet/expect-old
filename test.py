import unittest

from expecter import expect
from mock import Mock

from expect import new_expect


class ExpectTest(unittest.TestCase):

    class MyClass(object):
        @classmethod
        def classmethod(cls): pass

    def setUp(self):
        self.expect = new_expect()

    def tearDown(self):
        self.expect.reset()

    def test_delegates_to_eq(self):
        assert_equal = Mock(name='assert_equal')
        expect = new_expect(__eq__=assert_equal)
        expect('a') == 'b'
        assert_equal.assert_called_once_with('a', 'b')

    def test_stub_with_wrong_argument_raises_exception(self):
        self.expect(self.MyClass).stub('classmethod').with_(1)
        self.MyClass.classmethod(2)
        with expect.raises(AssertionError):
            self.expect.verify()

    def test_stub_returns_argument(self):
        self.expect(self.MyClass).stub('classmethod').with_(1).and_return(2)
        expect(self.MyClass.classmethod(1)) == 2

    def test_stub_does_not_raise_exception_if_not_called(self):
        self.expect(self.MyClass).stub('classmethod').with_(1).and_return(2)
        self.expect.verify()

    def test_mock_expectation_raises_exception_if_not_called(self):
        (self.expect(self.MyClass).should_receive('classmethod').with_(1)
                                   .and_return(2))
        with expect.raises(AssertionError):
            self.expect.verify()

    def test_stubs_and_resets_values(self):
        original_value = self.MyClass.classmethod
        self.expect(self.MyClass).stub('classmethod').with_(1).and_return(2)
        expect(self.MyClass.classmethod) != original_value
        self.expect.reset()
        expect(self.MyClass.classmethod) == original_value

    def test_repr_includes_argument(self):
        expect(repr(self.expect('a'))) == "expect('a')"

    def test_repr_without_argument_looks_ok(self):
        expect(repr(self.expect)) == 'expect'


if __name__ == '__main__':
    unittest.main()
