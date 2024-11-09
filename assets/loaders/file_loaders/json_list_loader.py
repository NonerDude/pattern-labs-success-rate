from __future__ import annotations
import json
import typing as t

from assets.loaders.file_loaders.file_lines_reader import FileLinesReader
import logging
logger = logging.getLogger(__name__)

class JSONListLoader():
    def __init__(self):
        self.file_loader = FileLinesReader()

    def load(self, path: str):
        """
        Loads given file and converts each line to a JSON object 

        Args:
            path (str): file to read json lines from

        Yields:
            t.Dict[t.Any]: yields object after object read line by line
        """
        for line in self.file_loader.read(path):
            obj = json.loads(line)
            logger.info(f"Object {obj} loaded")
            yield obj
