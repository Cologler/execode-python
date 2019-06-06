# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import tempfile

from pytest import raises

from execode.utils import find_pipfile, ensure_pipfile

def test_find_pipfile():
    path = find_pipfile(__file__)
    assert path.endswith('Pipfile')
    assert os.path.isfile(path)
    assert path == os.path.join(os.getcwd(), 'Pipfile')

    with tempfile.TemporaryDirectory() as tmpdir:
        assert find_pipfile(tmpdir) is None

def test_ensure_pipfile():
    path = ensure_pipfile(__file__)
    assert path.endswith('Pipfile')
    assert os.path.isfile(path)
    assert path == os.path.join(os.getcwd(), 'Pipfile')

    with tempfile.TemporaryDirectory() as tmpdir:
        with raises(FileNotFoundError):
            ensure_pipfile(tmpdir)
