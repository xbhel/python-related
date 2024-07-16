import logging
import os
import re
from dataclasses import dataclass

from extract_anchor import Anchor, PairedKeywordExtractor

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", logging.DEBUG),
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@dataclass
class TextNode:
    start_offset: int
    end_offset: int
    value: str
    node_index: int
    anchors: list[Anchor]


unenriched_texts = (
    "2.《中国人民共和国》(全国人民代表大会于1979年7月1日通过，1997年3月14日修订，1997年10月1日施行，2020年12月26日修正，《2021年3月1日起施行)",
    "纳税人采取欺骗》、隐藏手段进行虚假纳税申报或者不申报，逃避缴纳税款数额较大并且《占应纳税额百分之十以上》的，处三年以下有期徒刑或者拘役，《并处罚金》；数额巨大并且占应纳税额百分之三十以上的，处三年以上七年以下有期徒刑，并处罚金。",
    "第二百零一十一条 单位犯本节第二百零一条、第二百零三条、第二百零四条、第二百零七条、第二百零八条、《第二百零九条》规定之罪的，对单位判处罚金，并对其直接负责的主管人员和其他直接责任人员，依照各该条的规定处罚。",
)


def lambda_handler():
    # 1.concat all text nodes into a big string.
    body_text = str().join(unenriched_texts)

    # 2.spilt the str by specified delimiters.
    sentences = re.split(r"([。？！])", body_text)
    sentences = [''.join(vd) for vd in zip(sentences[0::2], sentences[1::2])]
    sentences.append('')  # ensure the last sentence is not missed.


    extractor = PairedKeywordExtractor((("《", "》"),))

    # 3.record the context of text node.
    start_offset = 0
    unenriched_text_nodes = []
    for index, text in enumerate(unenriched_texts):
        end_offset = len(text) + start_offset
        unenriched_text_nodes.append(
            TextNode(start_offset, end_offset, text, index, [])
        )
        start_offset = end_offset

    # 4.extract anchors from each sentence.
    start_index = 0
    extracted_anchors = []
    for sentence in sentences:
        anchors = extractor.extract(sentence)
        for anchor in anchors:
            anchor.start_index += start_index
            anchor.end_index += start_index
        start_index += len(sentence)
        extracted_anchors += anchors

    associate_text_nodes_for_anchors(unenriched_text_nodes, extracted_anchors)

    # 5.correctly set the anchor corresponded with text node by the context.
    for x in extracted_anchors:
        print(x)
    print("\n\n")
    for x in unenriched_text_nodes:
        print(x, "\n")

    start_index = 126 - 87
    end_index = 139 - 87
    s = "纳税人采取欺骗》、隐藏手段进行虚假纳税申报或者不申报，逃避缴纳税款数额较大并且《占应纳税额百分之十以上》的，处三年以下有期徒刑或者拘役，《并处罚金》；数额巨大并且占应纳税额百分之三十以上的，处三年以上七年 以下有期徒刑，并处罚金。"
    print(s[start_index:end_index])


def associate_text_nodes_for_anchors(
    unenriched_text_nodes: list[TextNode], anchors: list[Anchor]
):
    for anchor in anchors:
        has_match_text_node = False
        for text_node in unenriched_text_nodes:
            if (
                text_node.start_offset <= anchor.start_index
                and text_node.end_offset >= anchor.end_index
            ):
                has_match_text_node = True
                text_node.anchors.append(anchor)
                break
        if not has_match_text_node:
            logger.info(
                f"Unable to associate a suitable text node for anchor("
                f"{anchor.start_index}:{anchor.end_index}:{anchor.value}) in text node."
            )


if __name__ == "__main__":
    lambda_handler()
