# Python Beginners Guide

## Setting up a Python development environment

- Download and install Python3.

```bash
# The execution of the command below will install Python and set the environment variable on Windows.
$ scoop install python@3.11.9
```

- [Getting Started with Python in VS Code.](https://code.visualstudio.com/docs/python/python-tutorial#_install-and-use-packages)
    1. Here are some plugins that needed to be installed: Python, Python Debugger, isort, Python indent, Code Spell Checker, XML, markdownlint.

- [Use PyPI to install packages.](https://code.visualstudio.com/docs/python/python-tutorial#_install-and-use-packages)

```bash
py -m pip install numpy
```

- Use packages.

```python
import numpy as np

msg = "Roll a dice"
print(msg)

print(np.random.randint(1,9))
```

## Useful links

1. [Python Examples and Sample Code for Beginners.](https://wiki.python.org/moin/BeginnersGuide/Examples)
2. [PyPI - The Python Package Index.](https://pypi.org/)
3. [Python3 Document.](https://docs.python.org/3/tutorial/index.html)
4. [The standard Python library.](https://web.archive.org/web/20201017142948/http://effbot.org/zone/librarybook-index.htm)

## Required knowledge

1. Python packages manager: PyPI.
2. Python modules.
3. Make a package and store to a local repo by PyPI.
    - [How to upload a package to PIPY hub?](https://python-packaging-zh.readthedocs.io/zh-cn/latest/minimal.html#id2)
    - [github demo](https://github.com/cornradio/dumb_menu) & [blog](https://cornradio.github.io/hugo/posts/2023-02-18-python%E6%89%93%E5%8C%85/)
4. What are `__init__()` and `self` object in a class?
5. What is meaning of the `if __name__ == '__main__'`？
