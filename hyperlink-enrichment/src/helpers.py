import bisect
from collections import UserDict
from typing import OrderedDict, Sized

def isblank(text: str) -> bool:
    return text is None or text.isspace()


def isempty(coll: Sized) -> bool:
    return coll is None or len(coll) == 0


class ReadonlyNavigableDict(UserDict):
    """
    Implements a custom dict by extends UserDict instead of dict.
    UserDict is a convenient class that acts as a wrapper around dictionary objects.
    It's part of the collections module. UserDict is designed to be subclassed,
    allowing you to create your own dictionary-like classes with customized behavior.
    """

    def __init__(self, data: dict):
        self.data = OrderedDict(sorted(data.items(), key=lambda entry: entry[0]))
        self._keys = list(self.data.keys())

    def floor_key(self, key):
        """
        Returns The greatest key less than or equal to the given key, or None if there no such key.
        """
        sorted_keys = self._keys
        index = bisect.bisect_right(sorted_keys, key)
        if index:
            return sorted_keys[index - 1]

    def ceiling_key(self, key):
        """
        Returns the smallest key greater than or equal to the given key, or None if there no such key.
        """
        sorted_keys = self._keys
        index = bisect.bisect_left(sorted_keys, key)
        if index != len(sorted_keys):
            return sorted_keys[index]

    def floor_item(self, key):
        """
        Returns a key-value mapping associated with the greatest key less than or equal to the given key,
        or None if there is no such key.
        """
        k = self.floor_key(key)
        if k:
            return (k, self.data[k])

    def ceiling_item(self, key):
        """
        Returns a key-value mapping associated with the least key greater than or equal to the given key,
        or None if there is no such key.
        """
        k = self.ceiling_key(key)
        if k:
            return (k, self.data[k])

    def __setitem__(self, key, item):
        return self._readonly_error()

    def __delitem__(self, key):
        return self._readonly_error()

    def _readonly_error(self):
        raise AttributeError(
            "The ReadonlyNavigableDict does not support the modify operation."
        )