# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys

from fsoopify import FileInfo, NodeInfo, NodeType

def run_py(path: str, globals: dict=None, locals: dict=None):
    '''
    run a file like `python ?`.
    '''
    py_file = FileInfo(path)
    if not py_file.is_file():
        raise RuntimeError(f'{path} is not a file')

    sys.path.insert(0, py_file.path.dirname)
    if globals is None:
        globals = {}
    globals['__file__'] = py_file.path
    globals['__name__'] = '__main__'
    exec(py_file.read_text(), globals, locals)

def run_py_m(path: str, globals: dict=None, locals: dict=None):
    '''
    run a dir like `python -m ?`.
    '''
    node = NodeInfo.from_path(path)
    if not node:
        raise RuntimeError(f'{path} is not a file or dir')

    if node.node_type == NodeType.dir:
        pkg_dir = node # should be the dir which has a file __main__.py
        main_file = pkg_dir.get_fileinfo('__main__.py')
        if not main_file.is_file():
            raise RuntimeError(f'{main_file.path} is not a file')
    else:
        main_file = node # user may pass `pkg/__main__.py`
        pkg_dir = node.get_parent()

    sys.path.insert(0, pkg_dir.path.dirname)
    if globals is None:
        globals = {}
    globals['__file__'] = main_file.path
    globals['__name__'] = '__main__'
    globals['__package__'] = pkg_dir.path.name
    exec(main_file.read_text(), globals, locals)
