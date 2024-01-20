import util
from tmpl.context import Context


class Empty(Context):
    def __init__(self):
        super().__init__()


def test_init():
    #    with pytest.raises(NotImplementedError):
    Context()


def test_searchpath_context():
    # do_test_searchpath(Context())
    util.test_searchpath(Empty())
