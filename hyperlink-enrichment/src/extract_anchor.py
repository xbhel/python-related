import re
from abc import ABC, abstractmethod
from enum import Enum

import ahocorasick


class AnchorType(Enum):
    DATE = 0
    TITLE = 1
    ISSUE_NO = 2
    SELF_REF = 3
    ARTICLE_NO = 4
    ABBREVIATION = 5
    TRIAL_PROGRESS = 6


class Anchor:
    def __init__(self, value, start_index, end_index, type: AnchorType):
        self.value = value
        self.start_index = start_index
        self.end_index = end_index
        self.type = type

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


class BaseAnchorExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> list[Anchor]:
        """
        Extract the anchors from the given text.
        :params str text - the text to extract the anchors from.
        :return list[Anchor] - the list of anchors extracted from the text.
        """
        raise NotImplementedError()


class RegexAnchorExtractor(BaseAnchorExtractor):
    def __init__(self, patterns: list[str]):
        if patterns is None or len(patterns) == 0:
            raise ValueError("The patterns must be not empty!")
        self.patterns = patterns

    def extract(self, text: str) -> list[Anchor]:
        results = []
        for pattern in self.patterns:
            for m in re.finditer(pattern, text):
                results.append(Anchor(m.group(0), m.start(), m.end()))
        results.sort(key=lambda anchor: anchor.start_index)
        return results


def search(text: str, keywords: list) -> list[(str, int, int)]:
    """
    If overlapping keywords are given, the longest one will be returned. For example,
    if the keywords are ['Company', 'Company Law'], since the 'Company Law' is longer
    and contains the shorter keyword 'Company', the function will return 'Company Law'.
    """
    if is_blank(text):
        return

    automaton = ahocorasick.Automaton()
    for keyword in keywords:
        automaton.add_word(keyword, keyword)
    automaton.make_automaton()

    results = []
    for end_index, keyword in automaton.iter_long(text):
        # ensure the ending index is exclusive.
        end_index += 1  # type: ignore
        start_index = end_index - len(keyword)
        results.append((keyword, start_index, end_index))
    return results


def is_blank(text: str) -> bool:
    return isinstance(text, str) and text.isspace()
