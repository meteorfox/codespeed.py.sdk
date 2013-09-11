import StringIO
from nose.tools import assert_equal
from codespeed.sdk import Result
from codespeed.sdk import CodeSpeed

cs = Codespeed()

def test_list_servers():
    sl = cs.result
