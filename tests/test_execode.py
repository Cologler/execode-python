# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys

from execode import exec_pkg_py
from execode.utils import get_pyinfo

PKG1 = os.path.join('.', 'tests', 'dir_not_pkg', 'pkg1', 'sub_pkg', 'target.py')
PKG2 = os.path.join('.', 'tests', 'dir_not_pkg', 'pkg2.py')

def test_exec_pkg_py():
    g = exec_pkg_py(PKG1)
    assert g['value'] == 3
    assert 'pkg1' in sys.modules

def test_utils_get_pyinfo_pkg1():
    pyinfo = get_pyinfo(PKG1)
    assert pyinfo.path.endswith(
        os.path.join('tests', 'dir_not_pkg', 'pkg1', 'sub_pkg', 'target.py')
    )
    assert pyinfo.pkg_root.endswith(
        os.path.join('tests', 'dir_not_pkg', 'pkg1', '__init__.py')
    )
    assert pyinfo.pkg_name == '.'.join(['pkg1', 'sub_pkg'])
    assert pyinfo.name == '.'.join(['pkg1', 'sub_pkg', 'target'])

def test_utils_get_pyinfo_pkg2():
    pyinfo = get_pyinfo(PKG2)
    assert pyinfo.path.endswith(
        os.path.join('tests', 'dir_not_pkg', 'pkg2.py')
    )
    assert pyinfo.pkg_root.endswith(
        os.path.join('tests', 'dir_not_pkg', 'pkg2.py')
    )
    assert pyinfo.pkg_name == '.'.join(['pkg2'])
    assert pyinfo.name == '.'.join(['pkg2'])
