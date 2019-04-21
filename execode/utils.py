# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from typing import Union

from fsoopify import NodeType, NodeInfo, DirectoryInfo, FileInfo

def find_pipfile(node: Union[NodeInfo, str]):
    def _find_pipfile(dir: DirectoryInfo, deep: int):
        if deep == 0:
            return None
        pf = dir.get_fileinfo('Pipfile')
        if pf.is_file():
            return pf.path
        return _find_pipfile(dir.get_parent(), deep-1)

    if isinstance(node, str):
        node = NodeInfo.from_path(node)
        if not node:
            raise RuntimeError(f'{node} is not exists')
    elif node.node_type == NodeType.file:
        node = node.get_parent()

    return _find_pipfile(node, 10)

def find_pkg_root(node: Union[NodeInfo, str]):
    def _find_from_dir(node: DirectoryInfo):
        parent = node.get_parent()
        init = parent.get_fileinfo('__init__.py')
        if init.is_file():
            parent_init_path = _find_from_dir(parent)
            return parent_init_path if parent_init_path else init.path

    def _file_find_root(file: FileInfo):
        parent = file.get_parent()
        init = parent.get_fileinfo('__init__.py')
        if not init.is_file():
            return file.path # the file is single file package
        return _find_from_dir(file)

    if isinstance(node, str):
        node = NodeInfo.from_path(node)
        if not node:
            raise RuntimeError(f'{node} is not exists')

    if node.node_type == NodeType.file:
        return _file_find_root(node)
    else:
        return _find_from_dir(node)
