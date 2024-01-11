#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re
from typing import List
import logging
import csv
import urllib.request


with open('user_data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    PII_FIELDS = tuple(header[:5])


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    function that returns the log message
    args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
        all fields in the log line (message)
    """
    return re.sub(fr'({"|".join(fields)})=(.*?){re.escape(separator)}',
                  fr'\1={redaction}{separator}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initializing method"""
        super(RedactingFormatter, self).__init__(
            "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
        )
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format method"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """Create and configure a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger
