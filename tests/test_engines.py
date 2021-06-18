import imp
import os
import sys

import pytest
import util

import tmpl

engines = ["DjangoEngine", "Jinja2Engine"]
engines = ["DjangoEngine", "Jinja2Engine"]
scenarios = ["test0"]
env0 = {
    "envname": "env0",
    "int0": 42,
    "str0": "https://www.youtube.com/watch?v=qkc8YduPnOM",
}
env1 = {
    "envname": "env1",
    "int0": 24,
    "str0": "https://www.youtube.com/watch?v=qkc8YduPnOM",
}
envs = [env0]


class Engine:
    def __init__(self, name, scenario, env):
        self.name = name
        self.scenario = scenario
        self.env = env
        self.engine = getattr(tmpl, name, None)

        if not self.engine:
            pytest.skip("class %s not found" % (name))

        if not self.engine.can_load():
            pytest.skip("engine %s failed can_load" % (name))

        self.src_dir = os.path.join("tests", "data", f"{self.scenario}_{self.name}")
        self.expected_dir = os.path.join(
            "tests",
            "data",
            "expected",
            "{}-{}".format(self.scenario, self.env["envname"]),
        )
        print("src_dir=%s" % self.src_dir)
        print("expected_dir=%s" % self.expected_dir)

    def create_raw(self, **kwargs):
        return self.engine(**kwargs)

    def create(self, out_dir):
        return self.create_raw(
            tmpl_dir=str(self.src_dir), env=self.env, out_dir=str(out_dir)
        )


@pytest.fixture(params=scenarios)
def scenario(request):
    """
    test set
    """
    return request.param


@pytest.fixture(params=envs)
def env(request):
    """
    variable set / template context
    """
    return request.param


@pytest.fixture(params=engines)
def engine(request, scenario, env):
    """
    template engine
    """
    return Engine(request.param, scenario, env)


def test_init(engine):
    #  engine.create()
    engine.create("out_dir")


def test_init_missing(engine):
    #  engine.create()
    restore = sys.path
    sys.path = []
    assert not engine.engine.can_load()
    sys.path = restore


# def test_render_file_no_outdir(engine):
#    engine.create_raw()
#    eng.render('tmpl0', env0)
#
#    util.cmpdirs(engine.expected_dir, tmpdir)

# TODO missing tests
## render() doesn't have tmpl_dir
## jinja2 needs tmpl for init


def test_init_no_tmpl_dir(engine, tmpdir):
    eng = engine.create(tmpdir)
    # eng = engine.create_raw(tmpl_dir=str(self.src_dir), env=self.env, out_dir=str(out_dir))
    eng.render("tmpl0", env0)

    util.cmpfiles(engine.expected_dir, tmpdir, "tmpl0")


def test_get_template_noexist(engine, tmpdir):
    eng = engine.create(tmpdir)
    tmpl = eng.get_template("tmpl0")


def test_get_template_noexist(engine, tmpdir):
    eng = engine.create(tmpdir)
    with pytest.raises(LookupError):
        eng.get_template("noneexistant")


def test_render_file(engine, tmpdir):
    eng = engine.create(tmpdir)
    eng.render("tmpl0", env0)

    util.cmpfiles(engine.expected_dir, tmpdir, "tmpl0")


def test_render_string(engine, tmpdir):
    eng = engine.create(tmpdir)

    srcstr = open(os.path.join(engine.src_dir, "tmpl0")).read()
    expected = open(os.path.join(engine.expected_dir, "tmpl0")).read()
    assert expected == eng.render_string(srcstr)
    assert expected == eng.render_string(srcstr, env0)


def test_render_file_def_env(engine, tmpdir):
    eng = engine.create(tmpdir)
    eng.render("tmpl0")

    util.cmpfiles(engine.expected_dir, tmpdir, "tmpl0")


def test_render_walk(engine, tmpdir):
    eng = engine.create(tmpdir)


#    eng.render_walk()

#    util.cmpdirs(engine.expected_dir, tmpdir)


def test_render_walk_skip(engine, tmpdir):
    eng = engine.create(tmpdir)
    eng.render_walk(skip=r"^\.")

    util.cmpdirs(engine.expected_dir, tmpdir)


def test_searchpath(engine, tmpdir):
    ctx = engine.create_raw()
    util.test_searchpath(ctx)


def test_get_engine():
    for each in engines:
        assert getattr(tmpl, each) == tmpl.get_engine(each[:-6])


def test_get_engine_fail():
    with pytest.raises(KeyError):
        tmpl.get_engine("none")
