import logging

class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.INFO

class WarningFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.WARNING

class ErrorFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.ERROR

class DebugFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.DEBUG

class CriticalFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.CRITICAL
