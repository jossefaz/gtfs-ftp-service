#coding: utf-8

from logging.handlers import SMTPHandler as _SMTPHandler


class SMTPHandler(_SMTPHandler):

    def __init__(self, *args, **kwargs):
        super(SMTPHandler, self).__init__(*args, **kwargs)
        self._timeout = 30