import os
import inspect
import re

from dataclasses import dataclass
from lxml import etree
from lxml.etree import Element, ElementTree


@dataclass
class TextNode:
    node_id: int
    text: str
    node: Element
    type: int  # 0:text, 1 tail


def read_tree(filename: str) -> ElementTree:
    norm_rel_path = os.path.normpath(filename)
    current_location = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    file_path = os.path.join(current_location, norm_rel_path)
    return etree.parse(file_path)


class XMLContentHelper:

    def __init__(self, root: Element, ignore_tags=None):
        fake_root = Element('fake_root')
        fake_root.append(root)

        self._root = fake_root
        self.ignore_tags = ignore_tags or []
        self.text_nodes = self.get_text_nodes(fake_root)

    def get_text_nodes(self, element: Element, node_id: int = 0):
        text_nodes = []

        for child in element:
            if child.tag in self.ignore_tags:
                continue

            if self.__is_not_empty(child.text):
                text_nodes.append(TextNode(node_id, child.text, child, 0))
            if len(child):
                text_nodes.extend(self.get_text_nodes(child, node_id + 1))
            if self.__is_not_empty(child.tail):
                text_nodes.append(TextNode(node_id, child.tail, child, 1))

            node_id += 1

        return text_nodes

    @staticmethod
    def __is_not_empty(text: str):
        return text and not text.isspace()


def extract_anchors(unenriched_text_nodes: list[TextNode]):
    start_index = 0
    body_text = ''
    for text_node in unenriched_text_nodes:
        body_text += text_node.text

    sentences = re.split(r'([.])', body_text)
    sentences.append('')




if __name__ == '__main__':
    helper = XMLContentHelper(read_tree('../hyperlink/sample.xml').getroot())

    for node in helper.text_nodes:
        print(node)
