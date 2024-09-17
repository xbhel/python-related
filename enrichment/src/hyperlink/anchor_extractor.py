import re
import bisect
from collections import OrderedDict, UserDict
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeVar, Generic


class AnchorType(Enum):
    DATE = 0
    TITLE = 1
    ISSUE_NO = 2
    SELF_REF = 3
    ARTICLE_NO = 4
    ABBREVIATION = 5
    TRIAL_PROGRESS = 6


@dataclass
class Keyword:
    value: str
    start_index: int
    end_index: int

    def overlaps_with(self, other: "Anchor") -> bool:
        """
        Answer whether the given anchor overlaps this anchor instance.
        :params Anchor other - the other anchor to check for overlap.
        :return bool - True if the anchor overlap.
        """
        return (
                self.start_index <= other.end_index and self.end_index >= other.start_index
        )

    def contains(self, other: "Anchor") -> bool:
        """
        Answer whether this anchor contains the given anchor instance.
        :params Anchor other - the other anchor to check for contain.
        :return bool - True if the anchor contains the other anchor.
        """
        return (
                self.start_index <= other.start_index and self.end_index >= other.end_index
        )


@dataclass
class PairedKeyword(Keyword):
    value: str
    start_index: int
    end_index: int
    parent: "PairedKeyword" = field(init=False, repr=False, default=None, compare=False)
    children: list["PairedKeyword"] = None

    def add_child(self, child: "PairedKeyword"):
        if self.children is None:
            self.children = []
        self.children.append(child)


@dataclass
class Anchor(Keyword):
    value: str
    start_index: int
    end_index: int
    type: AnchorType
    parent: "Anchor" = field(init=False, default=None)
    version: str = field(init=False, default=None)


KT = TypeVar('KT')
VT = TypeVar('VT')


class ReadonlyNavigableDict(OrderedDict, Generic[KT, VT]):
    """
    Implements a custom dict by extends UserDict instead of dict.
    UserDict is a convenient class that acts as a wrapper around dictionary objects.
    It's part of the collections' module. UserDict is designed to be subclassed,
    allowing you to create your own dictionary-like classes with customized behavior.
    """

    def __init__(self, data):
        self.__readonly = False
        super().__init__(sorted(dict(data).items(), key=lambda x: x[0]))
        self.__readonly = True

    def floor_key(self, key: KT) -> KT:
        """
        Returns The greatest key less than or equal to the given key,
        or None if their no such key.
        """
        sorted_keys = list(self)
        index = bisect.bisect_right(sorted_keys, key)
        if index:
            return sorted_keys[index - 1]

    def ceiling_key(self, key: KT) -> KT:
        """
        Returns the smallest key greater than or equal to the given key,
        or None if their no such key.
        """
        sorted_keys = list(self)
        index = bisect.bisect_left(sorted_keys, key)
        if index != len(sorted_keys):
            return sorted_keys[index]

    def floor_item(self, key: KT) -> tuple[KT, VT]:
        """
        Returns a key-value mapping associated with the greatest key less than or equal to the given key,
        or None if there is no such key.
        """
        k = self.floor_key(key)
        if k is not None:
            return k, self.get(k)

    def ceiling_item(self, key: KT) -> tuple[KT, VT]:
        """
        Returns a key-value mapping associated with the least key greater than or equal to the given key,
        or None if there is no such key.
        """
        k = self.ceiling_key(key)
        if k is not None:
            return k, self.get(k)

    def __setitem__(self, key, item):
        self._readonly_error()
        super().__setitem__(key, item)

    def __delitem__(self, key):
        self._readonly_error()
        super().__delitem__(key)

    def _readonly_error(self):
        if self.__readonly:
            raise AttributeError(
                "The ReadonlyNavigableDict does not support the modify operation."
            )


class PairedKeywordExtractor:
    def __init__(self, pairs: dict[str, str]):
        if not pairs:
            raise ValueError("The pairs must be not empty.")
        self.pair_set = frozenset('|'.join(pair) for pair in pairs.items())
        self.pair_pattern = re.compile('|'.join(self.pair_set))

    def extract(self, text: str) -> list[PairedKeyword]:
        """
        Extract the keywords enclosed within pairs from the given text.
        :params str text - the text to extract the keywords from.
        :return list[PairedKeyword] - the list of keywords extracted from the text.
        """
        if not text:
            return []

        stack: list[tuple[int, str]] = []
        child_with_parent_index_dict: dict[int, int] = {}
        start_index_with_word_dict: dict[int, PairedKeyword] = {}
        for matcher in self.pair_pattern.finditer(text):
            cur = (matcher.start(), matcher.group())
            if stack and self.ispair(
                    (top := stack[-1])[1], cur[1]
            ):
                stack.pop()
                start_index, end_index = top[0], cur[0] + 1
                paired_word = PairedKeyword(
                    text[start_index:end_index], start_index, end_index
                )
                start_index_with_word_dict[start_index] = paired_word
                # That means either the pair is nested or half of the pair is missing.
                if stack:
                    parent_candidate_index, _ = stack[-1]
                    child_with_parent_index_dict[start_index] = parent_candidate_index
            else:
                stack.append(cur)
        # process the nested pair.
        for child_index, parent_index in child_with_parent_index_dict.items():
            child = start_index_with_word_dict[child_index]
            parent = start_index_with_word_dict[parent_index]
            if child and parent:
                child.parent = parent
                parent.add_child(child)
        return [
            v
            for _, v in sorted(
                start_index_with_word_dict.items(), key=lambda entry: entry[0]
            )
        ]

    def ispair(self, left, right) -> bool:
        return f"{left}|{right}" in self.pair_set


class TitleExtractor:
    __extractor = PairedKeywordExtractor({'《': '》'})

    def extract(self, content: str):
        outermost_anchors = []
        keywords = self.__extractor.extract(content)
        for keyword in keywords:
            if not keyword.parent:
                outermost_anchors.append(
                    Anchor(keyword.value, keyword.start_index, keyword.end_index, AnchorType.TITLE)
                )
        return outermost_anchors
