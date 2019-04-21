# execode

![GitHub](https://img.shields.io/github/license/Cologler/execode-python.svg)
[![Build Status](https://travis-ci.com/Cologler/execode-python.svg?branch=master)](https://travis-ci.com/Cologler/execode-python)
[![PyPI](https://img.shields.io/pypi/v/execode.svg)](https://pypi.org/project/execode/)

Tool for easy to run `.py`.

## API

API allow you run python code on current python runtime like use `exec` on code with correct globals info.

### execode.run_py()

run a file like `python ?` on command line.

### execode.run_py_m()

run a `__main__.py` like `python -m ?` on command line.

### execode.exec_pkg_py()

run a `.py` file inside a package.

the `.py` file can use relative import.

this is helpful for dynimic import some files.

### execode.pipenv_context

and you may want to use pipenv context like:

``` py
with execode.pipenv_context(THE_PIPFILE):
    execode.run_py(YOUR_FILE)
```
