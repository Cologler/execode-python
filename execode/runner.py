# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import runpy

from fsoopify import FileInfo, NodeInfo, NodeType
from .utils import use_path

def run_py(path: str):
    '''
    run a file like `python ?`.
    '''

    py_file = FileInfo(path)
    if not py_file.is_file():
        raise FileNotFoundError(f'{path} is not a file')

    with use_path(py_file.path.dirname):
        return runpy.run_path(py_file.path, run_name='__main__')

def run_py_m(path: str):
    '''
    run a dir like `python -m ?`.

    `runpy.run_module()` only run the module in `sys.path`,
    but `run_py_m` can run the module from any path.
    '''

    node = NodeInfo.from_path(path)
    if not node:
        raise FileNotFoundError(f'{path} is not a file or dir')

    if node.node_type == NodeType.dir:
        pkg_dir = node # should be the dir which has a file __main__.py
        main_file = pkg_dir.get_fileinfo('__main__.py')
        if not main_file.is_file():
            raise FileNotFoundError(f'{pkg_dir.path} is not a module')
    else:
        main_file = node # user may pass `pkg/__main__.py`
        pkg_dir = node.get_parent()

    with use_path(pkg_dir.path.dirname):
        return runpy.run_module(pkg_dir.path.name, run_name='__main__')

def exec_pkg_py(path: str):
    '''
    exec a `.py` file which inside a package.
    the `.py` file can use relative import.

    this is helpful for dynimic import some files.
    '''

    from .utils import get_pyinfo

    node = NodeInfo.from_path(path)
    if not node.is_file():
        raise FileNotFoundError(f'{path} is not a file')

    pyinfo = get_pyinfo(node)
    with use_path(pyinfo.get_sys_path_required()):
        return runpy.run_path(node.path, run_name=pyinfo.name)
