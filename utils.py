import sys
import os
from enum import Enum

DEBUG = True


def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )


class LogLevel(Enum):
    debug = 0
    info = 1
    silent = 2


class Logger:
    LOG_FORMAT = "[{}]: {}"

    def __init__(self, tag, logLevel=LogLevel.info, logFormat=LOG_FORMAT):
        self.logLevel = logLevel
        self.logFormat = str(logFormat)
        self.tag = tag

    def debug(self, msg):
        if(self.logLevel == LogLevel.debug):
            print self.logFormat.format(self.tag, msg)

    def info(self, msg):
        if not(self.logLevel == LogLevel.silent):
            print self.logFormat.format(self.tag, msg)
