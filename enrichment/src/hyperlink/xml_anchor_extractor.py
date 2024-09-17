import re

from lxml.etree import Element


def split_and_keep_separator(content: str, separators: list[str]):
    pattern = '|'.join(re.escape(x) for x in separators)
    # Ensure the separator is being remained
    values = re.split(f'({pattern})', content)
    # Ensure the last sentence is not missed
    values.append('')
    return [p + s for p, s in zip(values[0::2], values[1::2])]


def get_text_nodes(element: Element, node_id = 0, ignore_tags=None):
    pass
