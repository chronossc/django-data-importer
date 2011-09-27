# coding: utf-8


class UnknowSource(Exception):
    msg = u"The source file can't be opened"
    def __init__(self,err=None):
        if err:
            self.msg = u"%s, the error was: %s" % (self.msg,err)

