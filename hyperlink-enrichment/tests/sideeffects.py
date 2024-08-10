import logging
import os

from importmds import ImportHelper

ENV_MODE = os.getenv("ENV_MODE", "test")

def setup_logging():
    if ENV_MODE in ["dev", "test"]:
        logging.basicConfig(
            level=os.getenv("LOG_LEVEL", logging.DEBUG),
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
    else:
        logging.basicConfig(
            level=os.getenv("LOG_LEVEL", logging.DEBUG),
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename=os.getenv("LOG_FILENAME", "app.log"),
            filemode=os.getenv("LOG_FILEMODE", "a"),  # default: a -> append
        )


""" side effect: import the src module."""
setup_logging()
ImportHelper().import_src_module()
