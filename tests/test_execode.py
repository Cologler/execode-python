# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys

from execode import exec_pkg_py
from execode.pyinfo import get_pyinfo

PKG1 = os.path.join('.', 'tests', 'dir_not_pkg', 'pkg1', 'sub_pkg1', 'target.py')
PKG2 = os.path.join('.', 'tests', 'dir_not_pkg', 'pkg2.py')

def test_exec_pkg_py():
    g = exec_pkg_py(PKG1)
    assert g['value'] == 3
    assert 'pkg1' in sys.modules
    assert 'pkg1.mod1' in sys.modules

def test_utils_get_pyinfo_pkg1():
    pyinfo = get_pyinfo(PKG1)
    assert not pyinfo.is_top_module
    assert pyinfo.path.endswith(
        os.path.join('tests', 'dir_not_pkg', 'pkg1', 'sub_pkg1', 'target.py')
    )
    assert pyinfo.get_top_package().path.endswith(
        os.path.join('tests', 'dir_not_pkg', 'pkg1', '__init__.py')
    )
    assert pyinfo.get_parent_package().name == '.'.join(['pkg1', 'sub_pkg1'])
    assert pyinfo.name == '.'.join(['pkg1', 'sub_pkg1', 'target'])

def test_utils_get_pyinfo_pkg2():
    pyinfo = get_pyinfo(PKG2)
    assert pyinfo.is_top_module
    assert pyinfo.path.endswith(
        os.path.join('tests', 'dir_not_pkg', 'pkg2.py')
    )
    assert pyinfo.name == 'pkg2'
