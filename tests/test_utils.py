# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

from execode.utils import find_pipfile

def test_find_pipfile():
    path = find_pipfile(__file__)
    assert path.endswith('Pipfile')
    assert os.path.isfile(path)
    assert path == os.path.join(os.getcwd(), 'Pipfile')
