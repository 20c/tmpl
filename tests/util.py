
import filecmp
import os.path


def cmpfiles(expected_dir, actual_dir, files):
    if isinstance(files, basestring):
        files = [files]
    (match, mismatch, errors) = filecmp.cmpfiles(str(expected_dir), str(actual_dir), files, shallow=False)
    assert files == match
    assert not errors


def assert_dircmp(dcmp):
    assert not dcmp.diff_files
    assert not dcmp.common_funny
    assert not dcmp.funny_files
    assert not dcmp.left_only
    assert not dcmp.right_only

    for sub in dcmp.subdirs.values():
        assert_dircmp(sub)


def cmpdirs(expected, actual):
    """
    compare two directories and assert they're the same
    FIXME - filecmp.dircmp doesn't work with dotfiles, needs manual walk
    FIXME - does not recurse
    """

    dcmp = filecmp.dircmp(str(expected), str(actual))

    # print report for info on failures
    dcmp.report_full_closure()
    assert_dircmp(dcmp)


def test_searchpath(ctx):
    assert 0 == len(ctx.search_path)

    ctx.search_path = "tmpl"
    assert 1 == len(ctx.search_path)
    assert ["tmpl"] == ctx.search_path

    ctx.search_path = ["tmpl", "tmpl2"]
    assert 2 == len(ctx.search_path)
    assert ["tmpl", "tmpl2"] == ctx.search_path

    del ctx.search_path
    assert 0 == len(ctx.search_path)

