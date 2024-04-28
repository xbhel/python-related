"""
Note: You will catch a error if run directly a module which use the relative import.
-- https://zhiqiang.org/coding/python-path-faq.html
"""
from ..src.helpers import ImportHelper 

import_helper = ImportHelper()
import_helper.import_src_module()