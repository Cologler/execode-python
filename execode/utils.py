# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from typing import Union
from collections import namedtuple

from fsoopify import NodeType, NodeInfo, DirectoryInfo, FileInfo

def find_pipfile(node: Union[NodeInfo, str]):
    '''
    find the first parent dir which has `Pipfile`, return the path of the `Pipfile`.
    '''

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
            raise FileNotFoundError(f'{node} is not exists')

    if node.node_type == NodeType.file:
        node = node.get_parent()

    return _find_pipfile(node, 10)

PyInfo = namedtuple('PyInfo', [
    'path',
    'pkg_root',
    'pkg_name',
    'name',
])

def get_pyinfo(node: Union[NodeInfo, str]):
    store = {
        'pkg_root': None
    }
    pkg_parts = []
    name_parts = []

    def resolve_from_dir(node: DirectoryInfo):
        init = node.get_fileinfo('__init__.py')
        if init.is_file():
            store['pkg_root'] = init.path
            pkg_parts.append(node.path.name)
            name_parts.append(node.path.name)
            resolve_from_dir(node.get_parent())

    def resolve_from_file(node: FileInfo):
        store['pkg_root'] = node.path
        if node.path.name != '__init__.py':
            name_parts.append(node.path.name.pure_name)
        resolve_from_dir(node.get_parent())

    if isinstance(node, str):
        node = NodeInfo.from_path(node)
        if not node:
            raise FileNotFoundError(f'{node} is not exists')

    if node.node_type == NodeType.file:
        resolve_from_file(node)
    else:
        resolve_from_dir(node)

    store['path'] = node.path

    pkg_parts.reverse()
    name_parts.reverse()

    if pkg_parts:
        store['pkg_name'] = '.'.join(pkg_parts)
    else:
        store['pkg_name'] = node.path.name.pure_name
    store['name'] = '.'.join(name_parts)

    return PyInfo(**store)


def find_pkg_root(node: Union[NodeInfo, str]):
    '''
    find the top level dir which has `__init__.py`, return the path of the `__init__.py`.
    if `node` is not in a package, return the path of the `node`.
    '''

    return get_pyinfo(node).pkg_root

def get_pkg_name(node: Union[NodeInfo, str]):
    '''
    get the package name of the `node`.
    if `node` is not in a package, return the name of the `node`.
    '''

    return get_pyinfo(node).pkg_name
