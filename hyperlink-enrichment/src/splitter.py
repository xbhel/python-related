from enum import Enum, auto, unique
import logging
import os
from xml.etree.ElementTree import fromstring

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", logging.DEBUG),
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@unique
class DocSchema(Enum):
    LEGIS = []
    Case = auto()
    SECLAW = auto()
    AP = []
    NEWS = ()

    def __init__(self, subs: list[str]) -> None:
        self.subs = subs

    @classmethod
    def of(cls, name):
        for schema in DocSchema:
            if name in schema.subs:
                return schema


SCHEMA_WITH_RELEASE_DATE_MAP = {
    "legis": "date",
    "funddoc": "date",
    "regulation": "date",
    "courtrule": "issue_date",
    "seclaw": "promulgation_date",
    "courtcase": "issue_date",
    "newsitem": "promulgation_date",
}

DOC_META_XPATH_MAP = {}


def extract_doc_meta(index_id: str, schema: str) -> dict:
    try:
        xpath_prop_map = {v: k for k, v in DOC_META_XPATH_MAP}
        schema == "admindoc" and xpath_prop_map.pop("release_date")
        x_nodes = edms_get_nodes_batch(
            index_id, {"xpaths": [{"xpath": x} for x in list(xpath_prop_map)]}
        )

        doc_meta = {}
        for x_node in x_nodes:
            value = ""
            nodes = x_node.get("nodes")
            prop = xpath_prop_map.get(x_node.get("xpath"))
            if nodes:
                value = nodes[0]["data"]
            else:
                logger.warning(f"Cannot find the {prop} of doc in the index {index_id}")
            doc_meta[prop] = value

        meta_items = fromstring(doc_meta["metadata"]).findall(".//metaitem")
        doc_meta["metadata"] = {x["name"]: x["value"] for x in meta_items}
        doc_meta["release_date"] = doc_meta.get(
            "release_date", doc_meta["meta_data"].get(SCHEMA_WITH_RELEASE_DATE_MAP[schema])
        )
        
    except Exception as e:
        logger.error(f'Error occurred in extract_docmeta: Exception --> {e}')
    return doc_meta


def edms_get_nodes_batch(index_id, body):
    pass
