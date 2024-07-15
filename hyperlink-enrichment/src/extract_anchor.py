import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import overload

import ahocorasick
from helpers import isblank, isempty

REGEX_OR = "|"


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


class PairedKeywordExtractor:
    def __init__(self, pairs: dict[str, str]):
        if isempty(pairs):
            raise ValueError("The pairs must be not empty.")
        self.pair_set = frozenset(REGEX_OR.join(pair) for pair in pairs)
        self.pair_pattern = re.compile(REGEX_OR.join(self.pair_set))

    def extract(self, text: str) -> list[PairedKeyword]:
        """
        Extract the keywords enclosed within pairs from the given text.
        :params str text - the text to extract the keywords from.
        :return list[PairedKeyword] - the list of keywords extracted from the text.
        """
        if isblank(text):
            return []

        stack: list[tuple[int, str]] = []
        child_with_parent_index_dict: dict[int, int] = {}
        start_index_with_word_dict: dict[int, PairedKeyword] = {}
        for matcher in self.pair_pattern.finditer(text):
            cur = (matcher.start(), matcher.group())
            if len(stack) != 0 and self.ispair(
                (top := stack[len(stack) - 1])[1], cur[1]
            ):
                stack.pop()
                start_index, end_index = top[0], cur[0] + 1
                paired_word = PairedKeyword(
                    text[start_index:end_index], start_index, end_index
                )
                start_index_with_word_dict[start_index] = paired_word
                # That means either the pair is nested or half of the pair is missing.
                if len(stack) != 0:
                    (parent_candidate_index, _) = stack[len(stack) - 1]
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

    def ispair(self, symbol1, symbol2) -> bool:
        return (
            f"{symbol1}{REGEX_OR}{symbol2}" in self.pair_set
            or f"{symbol2}{REGEX_OR}{symbol1}" in self.pair_set
        )


class AbsAnchorExtractor(ABC):
    @overload
    @abstractmethod
    def extract(self, text: str):
        """
        Extract the anchors from the given text.
        :params str text - the text to extract the anchors from.
        :return list[Anchor] - the list of anchors extracted from the text.
        """

    @overload
    def extract(
        self, text: str, dependencies: dict[AnchorType, list[Anchor]]
    ) -> list[Anchor]:
        if isblank(text):
            return []
        anchors = self.extract(text)
        if any(isempty(e) for e in (anchors, dict)):
            return anchors
        for d_type, d_anchors in dependencies.items:
            if not isempty(d_anchors):
                self._remove_overlap_anchors_with_dependencies(anchors, d_anchors)
                self._associate_anchors_with_dependencies(anchors, (d_type, d_anchors))

    @abstractmethod
    def _associate_anchors_with_dependencies(
        self, anchors: list[Anchor], dep: tuple[AnchorType, list[Anchor]]
    ): ...

    def _remove_overlap_anchors_with_dependencies(
        self, anchors: list[Anchor], dep_anchors: list[Anchor]
    ):
        for anchor in iter(anchors):
            any(
                anchor.overlaps_with(d_anchor) for d_anchor in dep_anchors
            ) and anchors.remove(anchor)


class RegexAnchorExtractor(AbsAnchorExtractor):
    def __init__(self, patterns: list[str]):
        if isempty(patterns):
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
    if isblank(text):
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
