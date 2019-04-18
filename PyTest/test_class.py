#Content of test_class.py
import pytest

class TestClass(object):
    def test_one(self):
        x = "this"
        assert 'h' in x
    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')
    def test_needsfiles(tmpdir):
       print (tmpdir)
       assert 0
    def f():
      raise SystemExit(1)
    def test_mytest():
      with pytest.raises(SystemExit):
          f() 
