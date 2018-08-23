# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import collections
import contextlib
import errno
import os
import sublime, sublime_plugin
import sys
import zipfile

PLUGIN_NAME = "Extract Sublime Package"
PACKAGE_EXT = ".sublime-package"

str_type = str if sys.version_info[0] >= 3 else unicode

# decorator that manages function-level "globals" (like static in C functions)
def functionlocals(spec):
    if isinstance(spec, str_type):
        spec = spec.split(" ")
    class _FuncLocals(object):
        def __setattr__(self, name, attr):
            if name in spec:
                object.__setattr__(self, name, attr)
            else:
                raise AttributeError("invalid attribute '%s'" % name)

    def _make_functionlocals(f):
        _locals = _FuncLocals()
        def _wrapper(*args, **kwargs):
            return f(_locals, *args, **kwargs)
        return _wrapper

    return _make_functionlocals


def is_a_package(filename):
    return filename is not None and os.path.splitext(filename)[1] == PACKAGE_EXT

# get and cache Packages mode
@functionlocals("dir_mode")
def packages_dir_mode(funclocals):
    try:
        return funclocals.dir_mode
    except AttributeError:
        p = sublime.packages_path()
        funclocals.dir_mode = os.stat(p).st_mode
        return funclocals.dir_mode

def _msg(msg):
    sublime.status_message("%s: %s" % (PLUGIN_NAME, msg))


def extract_package(filename, spcpath=""):
    base_name = os.path.basename(filename)
    dir_base_name = os.path.splitext(base_name)[0]
    print(sublime.packages_path())
    if spcpath != "":
        outdir = os.path.join(spcpath, dir_base_name)
    else:
        outdir = os.path.join(sublime.packages_path(), dir_base_name)
    try:
        arc = zipfile.ZipFile(filename)
    except zipfile.BadZipfile:
        # can't open the file
        _msg("package file %s is invalid" % base_name)
    with contextlib.closing(arc):
        try:
            os.mkdir(outdir, packages_dir_mode())
        except OSError:
            if os.path.isdir(outdir) and len(os.listdir(outdir)) == 0:
                # directory existed, but was empty; continuing
                pass
            else:
                # so this isn't great, let's abort
                _msg("directory Packages/%s couldn't be created or wasn't empty" %
                     dir_base_name)
                return
        try:
            arc.extractall(outdir)
        except:
            # so something else altogether went wrong
            _msg("extracting %' failed" % base_name)
            return
        _msg("%s extracted" % base_name)
    



class ExtractCurrentPackageFileCommand(sublime_plugin.WindowCommand):
    def run(self, path=""):
        view = self.window.active_view()
        if view is not None:
            extract_package(view.file_name(), path)

    def is_enabled(self):
        view = self.window.active_view()
        return is_a_package(view.file_name()) if view is not None else False

    def is_visible(self):
        return self.is_enabled()


class ExtractSinglePackageFileCommand(sublime_plugin.WindowCommand):
    def run(self, files, path=""):
        extract_package(files[0], path)

    def is_enabled(self, files):
        return len(files) == 1 and is_a_package(files[0])

    def is_visible(self, files):
        return self.is_enabled(files)

class ExtractAllPackagesCommand(sublime_plugin.WindowCommand):
    def run(self, path=""):

        multi_importer = sublime_plugin.multi_importer
        zippaths = []
        for loader in multi_importer.loaders:
            zippath = loader.zippath
            if is_a_package(zippath):
                zippaths.append(zippath)

        zippaths_total = len(zippaths)
        if sublime.ok_cancel_dialog("Extract %s to the Packages directory? This may take a while."
                                    % zippaths_total):
            for zippath in zippaths:
                extract_package(zippath, path)
            _msg("Completed extracting %s packages" % zippaths_total)


class ExtractPackageFilesCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        for filename in files:
            extract_package(filename)

    def is_enabled(self, files):
        return len(files) > 1 and all(is_a_package(f) for f in files)
    
    def is_visible(self, files):
        return self.is_enabled(files)

class ExtractLoadedPackageFileEventListener(sublime_plugin.EventListener):
    def on_load(self, view):
        global_settings = sublime.load_settings("Preferences.sublime-settings")
        ask_on_open = global_settings.get("extract_sublime_package_ask_on_open", False)
        filename = view.file_name()
        if is_a_package(filename) and ask_on_open:
            if sublime.ok_cancel_dialog("Extract %s to the Packages directory?"
                                        % os.path.basename(filename)):
                extract_package(filename)
