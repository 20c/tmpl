
import filecmp
import imp
import os
import pytest
import sys

from twentyc.tmpl.context import Context
import util


class Empty(Context):
    def __init__(self):
        super(Empty, self).__init__()

def test_init():
#    with pytest.raises(NotImplementedError):
    Context()


def test_searchpath_context():
    #do_test_searchpath(Context())
    util.test_searchpath(Empty())

