import os
import re
import inspect
from dataclasses import dataclass

from lxml import etree
from lxml.etree import Element, ElementTree
from anchor_extractor import TitleExtractor, ReadonlyNavigableDict, Keyword, Anchor


@dataclass
class Text:
    node_id: int
    value: str
    type: str


@dataclass
class TextNode(Keyword):
    text: Text
    anchors: list[Anchor]


class Texts:

    def __init__(self, root, ignore_tags=None):
        fake_root = Element('fake__root')
        fake_root.append(root)
        self.__root = fake_root
        self.ignore_tags = ignore_tags or []
        self.text_nodes = self.__get_text_nodes(fake_root)

    def get_node(self, node_id) -> Element:
        return list(self.__root[0].iter())[node_id]

    def get_nodes(self, start_node_id, end_node_id) -> list[Element]:
        return list(self.__root[0].iter())[start_node_id:end_node_id]

    def __get_text_nodes(self, element: Element, node_id: int = 0) -> list[Text]:
        text_nodes = []
        ignore_tags = self.ignore_tags

        for child in element:
            if child.tag not in ignore_tags:
                if child.text and not child.text.isspace():
                    text_nodes.append(Text(node_id, child.text, 'text'))

                if len(child):
                    text_nodes.extend(self.__get_text_nodes(child, node_id + 1))

                if child.tail and not child.tail.isspace():
                    text_nodes.append(Text(node_id, child.tail, 'tail'))

            node_id += 1

        return text_nodes


def read_xml(filename: str) -> ElementTree:
    norm_rel_path = os.path.normpath(filename)
    current_location = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    file_path = os.path.join(current_location, norm_rel_path)
    return etree.parse(file_path)


def split(content: str, separators: list[str]):
    pattern = '|'.join(re.escape(x) for x in separators)
    # Ensure the separator is being remained
    parts = re.split(f'({pattern})', content)
    # Ensure the last sentence is not missed
    parts.append('')
    return [p + s for p, s in zip(parts[0::2], parts[1::2])]


def extract_anchors_by_sentence(content: str):
    extractor = TitleExtractor()
    sentences = split(content, ['。'])

    result = []
    start_index = 0
    for sentence in sentences:
        anchors = extractor.extract(sentence)
        for anchor in anchors:
            anchor.start_index += start_index
            anchor.end_index += start_index
        start_index += len(sentence)
        result += anchors

    return result


def extract_anchors_from_xml(element):
    texts = Texts(element)

    # concat the content
    content = ''
    text_nodes = []
    start_index = 0
    for text in texts.text_nodes:
        content += text.value
        end_index = len(text.value) + start_index
        text_nodes.append(TextNode(text.value, start_index, end_index, text, []))
        start_index = end_index

    anchors = extract_anchors_by_sentence(content)
    nav = ReadonlyNavigableDict[int, TextNode]({x.start_index: x for x in text_nodes})

    for anchor in anchors:
        _, head = nav.floor_item(anchor.start_index)
        _, tail = nav.floor_item(anchor.end_index - 1)

        if head == tail:
            head.anchors.append(anchor)
            continue

        if tail.text.type == 'tail':
            head_element = texts.get_node(head.text.node_id)
            tail_element = texts.get_node(tail.text.node_id)

            is_parent = tail_element.getparent() == head_element and head.text.type == 'text'
            is_contained = tail_element.getparent() == head_element.getparent() and head.text.type == 'tail'
            if is_parent or is_contained:
                head.anchors.append(anchor)
                tail.anchors.append(anchor)

    return text_nodes


if __name__ == '__main__':
    extract_anchors_from_xml(read_xml('sample.xml').getroot())
