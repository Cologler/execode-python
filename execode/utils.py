# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
from typing import Union
from collections import namedtuple
import contextlib
import abc

from fsoopify import NodeType, NodeInfo, DirectoryInfo, FileInfo, Path

def find_pipfile(node: Union[NodeInfo, str], depth: int = 10) -> Path:
    '''
    find the first parent dir which has `Pipfile`, return the path of the `Pipfile`.
    '''

    def _find_pipfile(dir: DirectoryInfo, depth: int):
        if depth == 0:
            return None
        pf = dir.get_fileinfo('Pipfile')
        if pf.is_file():
            return pf.path
        return _find_pipfile(dir.get_parent(), depth-1)

    if isinstance(node, str):
        node = NodeInfo.from_path(node)
        if not node:
            raise FileNotFoundError(f'{node} is not exists')

    if node.node_type == NodeType.file:
        node = node.get_parent()
        depth -= 1

    return _find_pipfile(node, depth)


@contextlib.contextmanager
def use_path(path):
    is_insert = path not in sys.path
    if is_insert:
        sys.path.insert(0, path)
    yield
    if is_insert:
        try:
            sys.path.remove(path)
        except ValueError:
            pass
