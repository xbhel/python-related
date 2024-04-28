import inspect
import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.DEBUG))


class ImportHelper:
    """
    The python interpreter will use follows rules to find a module when you import it:
    1. built-in modules: Python first searches for the module in its built-in modules, which are part of the Python installation.
    2. Directories in sys.path: If the module is not found among the built-in modules, Python searches for it in the directories specified
      in the sys.path variable. sys.path is initialized from the PYTHONPATH environment variable, plus an installation-dependent default.
    3. Current Directory: Python also checks the directory from which the script is run.
    4. Site Packages: Additionally, Python searches in the directories contained in the site-packages folder of the Python installation.
    5. Package init.py: If a module is part of a package (i.e., the module is in a directory containing a file named __init__.py),
      Python imports the __init__.py file first, and then continues searching for the module within the package.

    reference: https://docs.python.org/zh-cn/3/reference/import.html
    """

    def __init__(self, project_name=""):
        """
        In Python, naming a field with a double underscore prefix (__) indicates that it's intended to be a private field.
        This convention is used to suggest that the field should not be accessed or modified directly from outside the class.
        However, it's important to note that this is just a convention, and Python doesn't enforce privacy like some other languages do.
        """
        self.__project_name = project_name
        self.__tests_dir_aliases = ("tests", "Tests", "test")
        self.__source_dir_aliases = ("src", "source", "Source")
        # obtain the absolute path of current file
        self.__current_location = inspect.stack()[0][1]

    def import_module(self, module_paths: list[str]):
        root_path = self.get_root_path()
        for module_path in module_paths:
            if os.path.exists(_path := os.path.join(root_path, module_path)):
                sys.path.append(_path)
                return
            else:
                logger.error(
                    "Cannot locate the {} module, please ensure it is a valid module.".format(
                        _path,
                    )
                )

    def import_src_module(self):
        root_path = self.get_root_path()
        source_dir_aliases = self.__source_dir_aliases
        for alias in source_dir_aliases:
            if os.path.exists(src_path := os.path.join(root_path, alias)):
                sys.path.append(src_path)
                return
        logger.error(
            "Cannot locate the valid src module, and its default aliases are [{}].".format(
                ",".join(source_dir_aliases)
            )
        )

    def get_root_path(self) -> str:
        project_name = self.__project_name
        current_location = self.__current_location
        subdir_possible_of_root = (
            *self.__source_dir_aliases,
            *self.__tests_dir_aliases,
        )

        if project_name:
            index = current_location.find(project_name)
            return current_location[: index + len(project_name)]

        current_dir = os.path.abspath(os.path.join(current_location, ".."))
        dir_num = len(current_dir.split(os.sep))

        if current_dir.endswith(
            tuple(os.sep + src_dirname for src_dirname in subdir_possible_of_root)
        ):
            return os.path.abspath(os.path.join(current_dir, ".."))

        root_dir = current_dir
        while dir_num:
            for src_dirname in subdir_possible_of_root:
                if os.path.exists(os.path.join(root_dir, src_dirname)):
                    return root_dir
            root_dir = os.path.abspath(os.path.join(root_dir, ".."))

        raise RuntimeError(
            "Cannot locate the root path. You may be need to set the project_name:{}, \
                src_dir_alias:{} and test_dir_alias:{} to assist us in locating the root path.".format(
                project_name, self.__source_dir_aliases, self.__tests_dir_aliases
            )
        )

    @property
    def source_dir_aliases(self):
        return self.__source_dir_aliases

    @source_dir_aliases.setter
    def source_dir_aliases(self, value: tuple):
        self.__source_dir_aliases = value

    @property
    def tests_dir_aliases(self):
        return self.__tests_dir_aliases

    @tests_dir_aliases.setter
    def tests_dir_aliases(self, value: tuple):
        self.__tests_dir_aliases = value

class TreeDict(dict):
    pass

if __name__ == "__main__":
    helper = ImportHelper()
    print(helper.get_root_path())
    print(helper.source_dir_aliases, helper.tests_dir_aliases)
    helper.source_dir_aliases, helper.tests_dir_aliases = ('src',), ('test',)
    print(helper.source_dir_aliases, helper.tests_dir_aliases)

