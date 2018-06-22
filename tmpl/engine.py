from __future__ import (absolute_import, division, print_function)
from past.builtins import basestring

from tmpl import context


class Jinja2Template(context.Template):
    def __init__(self, tmpl, **kwargs):
        self.tmpl = tmpl
        super(Jinja2Template, self).__init__(**kwargs)

    def render(self, env):
        """
        renders from template, return object
        """

        return self.tmpl.render(env)

    def load(self):
        pass
    def loads(self):
        pass


class Jinja2Engine(context.Context):

    """template interface class for jinja2"""

    @staticmethod
    def can_load():
        import imp

        try:
            imp.find_module('jinja2')
            return True

        except ImportError:
            return False

    def __init__(self, **kwargs):
        import jinja2

        super(Jinja2Engine, self).__init__(**kwargs)

        self.engine = jinja2.Environment(loader=jinja2.FileSystemLoader(self._search_path))
        self.engine.line_statement_prefix = '.'
        self.engine.line_comment_prefix = ';.'
        self.engine.keep_trailing_newline = True
        self.engine.lstrip_blocks = True
        self.engine.trim_blocks = True

    @property
    def search_path(self):
        return self.engine.loader.searchpath

    @search_path.setter
    def search_path(self, path):
        if isinstance(path, basestring):
            self._search_path = [path]
            self.engine.loader.searchpath = [path]
        else:
            self.engine.loader.searchpath = path

    @search_path.deleter
    def search_path(self):
        self.engine.loader.searchpath = []

        #self.engine.loader.searchpath = path

    def get_template(self, name):
        """ finds template in search path
            returns Template object
        """
        return Jinja2Template(Jinja2Template(self.engine.get_template(name)))

    def make_template(self, tmpl_str):
        """ makes template object from a string """
        return Jinja2Template(Template(tmpl_str))

    def _render(self, src, env):
        """
        renders from template, return object
        """

        return self.engine.get_template(src).render(env)

    def _render_str_to_str(self, instr, env):
        """
        renders from template, return object
        """

        return self.engine.from_string(instr).render(env)


class DjangoTemplate(context.Template):
    def __init__(self, tmpl, **kwargs):
        self.tmpl = tmpl
        super(DjangoTemplate, self).__init__(**kwargs)

    def render(self, env):
        """
        renders from template, return object
        """
        from django.template import Context

        return self.tmpl.render(Context(env))

    def load(self):
        pass
    def loads(self):
        pass


class DjangoEngine(context.Context):

    """template interface class for Django"""

    @staticmethod
    def can_load():
        import imp

        try:
            imp.find_module('django')
            return True

        except ImportError:
            print("import error")
            return False

    def __init__(self, **kwargs):
        import django.template
        import django
        from django.conf import settings
        from django.template import Template

        if not settings.configured:
            settings.configure(
                TEMPLATES=[
                    {
                        'BACKEND':
                        'django.template.backends.django.DjangoTemplates'
                    }
                ]
            )
            django.setup()

        self.tmpl_ctor = Template
        super(DjangoEngine, self).__init__(**kwargs)

    def get_template(self, name):
        filename = self.find_template(name)
        if not filename:
            raise LookupError("template not found")
        return self.make_template(open(filename).read())

    def make_template(self, tmpl_str):
        """ makes template object from a string """
        return DjangoTemplate(self.tmpl_ctor(tmpl_str))

    def _render_str_to_str(self, instr, env):
        """
        renders contents of instr with env returns string
        """

        return self.make_template(instr).render(env)
