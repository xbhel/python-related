import re
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


def search(text: str, pattern: str) -> list[(str, int, int)]:  # type: ignore
    if not pattern:
        raise RuntimeError("The pattern must be not none.")
    if is_blank(text):
        return
    results = []
    for matcher in re.finditer(pattern, text):
        results.append((matcher.group(0), matcher.start(), matcher.end()))
    return results


def is_blank(text: str) -> bool:
    return isinstance(text, str) and text.isspace()


print(search("hello <java> or <csharp>", "(<[^><]*>)"))
list = (1, 2, 3)
a, *b = list
print(a)
print(b)
