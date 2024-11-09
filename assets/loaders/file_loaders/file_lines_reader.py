import typing as t

import logging
logger = logging.getLogger(__name__)

class FileLinesReader:
    def read(self, path: str):
        """_summary_

        Args:
            path (str): file to read line by line

        Raises:
            FileNotFoundError: Given file is not found

        Yields:
            Iterator[t.Iterable[str]]: line by line of given file path
        """
        try:
            logger.info(f"Opening file {path} to be read line by line")
            with open(path,  'r') as file:
                for index, line in enumerate(file.readlines()):
                    line = line.rstrip('\n')
                    logger.info(f"File {path} {index} line: line")
                    yield line
        except FileNotFoundError as not_found:
            logger.error(f"File {file} not found")
            raise Exception(not_found, f"File {file} not found")
