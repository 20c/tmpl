from __future__ import (absolute_import, division, print_function)
from builtins import (object, str)
from past.builtins import basestring

import os
import re


class RenderError(Exception):
    pass


class Context(object):
    """generic template interface class """

    def __init__(self, **kwargs):
        """
        tmpl_dir is the base directory templates are stored in
        out_dir is the output directory
        env is a default set of variables to use
        """

        self._search_path = []
        if 'tmpl_dir' in kwargs:
            self._search_path = [kwargs.get('tmpl_dir')]

        if 'search_path' in kwargs:
            self._search_path = kwargs.get('search_path', [])

        self.out_dir = kwargs.get('out_dir', None)
        self.env = kwargs.get('env', {})

    @property
    def search_path(self):
        return self._search_path

    @search_path.setter
    def search_path(self, path_list):
        if isinstance(path_list, basestring):
            self._search_path = [path_list]
        else:
            self._search_path = path_list

    @search_path.deleter
    def search_path(self):
        self._search_path = []

# overridden if engine can handle it, otherwise we mock
#    def get_template(self, name):
#        filename = self.find_template(name)
#        if not filename:
#            raise LookupError("template not found")
#        return filename

    def find_template(self, name):
        for tmpl_dir in self.search_path:
            tmpl_file = os.path.join(tmpl_dir, name)
            if os.path.exists(tmpl_file):
                return tmpl_file
        return None

    def render(self, src, env=None, out_dir=None, out_file=None):
        """
        renders src.tmpl with env to produce out_dir/src
        """
        if not env:
            env = self.env
        if not out_dir:
            out_dir = self.out_dir

        if out_file:
            dest = out_file
        else:
            if not out_dir:
                raise RenderError("no output directory (out_dir) set")

            dest = os.path.join(str(out_dir), src)

        if not out_dir:
            raise RenderError("no output directory (out_dir) set")

        print(self.out_dir)
        print(src)
        print(os.getcwd())

        self._render_file(src, env, dest)

    def render_file(self):
        pass

    def render_env(self, env=None):
        if not env:
            env = self.env

    def render_string(self, instr, env=None):
        """
        renders instr string with env and returns output string
        """
        if not env:
            env = self.env
        return self._render_str_to_str(instr, env)

    def render_walk(self, env=None, prefix='', skip=None, tmpl_dir=None, out_dir=None):
        """
        Walks a directory and recursively renders all files

        env -- override environment [default: self.env]
        skip -- list of regex to skip files [default: None]
                matches against the whole relative source path and the filename
        prefix -- prefix output file with this [default: '']

        returns a list generated files tuples (source, output)
        """

        if not env:
            env = self.env
        if not out_dir:
            out_dir = self.out_dir

        if tmpl_dir:
            return self.__render_walk(env, tmpl_dir, out_dir, prefix=prefix, skip=skip)

        for tmpl_dir in self.search_path:
            self.__render_walk(env, tmpl_dir, out_dir, prefix=prefix, skip=skip)

    def __render_walk(self, env, tmpl_dir, out_dir, prefix, skip):

        if skip:
            skip_re = re.compile(skip)

        generated = []

        #self.debug_msg("rendering " + prefix + " from " + tmpl.tmpl_dir + " to " + tmpl.out_dir)
        for root, dirs, files in os.walk(tmpl_dir):
            rel_dir = os.path.relpath(root, tmpl_dir)
            if rel_dir == '.':
                rel_dir = ''
            elif skip and skip_re.search(rel_dir):
                continue

            out_dir = os.path.join(out_dir, prefix)
            for file in files:
                if skip and skip_re.search(file):
                    continue

                #self.debug_msg("rendering from " + file)

                targ_dir = os.path.join(out_dir, rel_dir)
                if not os.path.exists(targ_dir):
                    os.makedirs(targ_dir)
                dest_file = os.path.join(targ_dir, file)
                generated.append(dest_file)
                env["filename"] = os.path.join(rel_dir, prefix + file)
                #self.debug_msg("generating file " + env['filename'])
                #self.render(os.path.join(rel_dir, file), out_file=dest_file, env=env)
                self.render(os.path.join(rel_dir, file), out_file=dest_file, env=env)

        return generated

    def _render(self, src, env):
        """
        renders src template file with env to return string
        """

        abs_path = self.find_template(src)
        return self._render_str_to_str(open(abs_path).read(), env)

    def _render_file(self, src, env, dest):
        """
        renders src template with env to produce dest file
        """

        open(dest, "w").write(self._render(src, env))

    def dump(self, src, env):
        tmpl = self.ctx.get_template(src)
        print(tmpl.render(env))


class Template(object):
    def __init__(self, **kwargs):
        pass
      #self.src = file, string, obj
      #self.ctx = Context

    def render_string(self):
        pass

    def render_file(self):
        pass
