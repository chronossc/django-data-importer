# coding: utf-8

import logging

# define a null logging handler, like in py 2.7 docs: 
# http://docs.python.org/library/logging.handlers.html#nullhandler
# useful for no output in tests if you don't need to test logging.
class NullHandler(logging.Handler):
    def emit(self,record):
        pass

    def handle(self,record):
        pass

    def createLock(self):
        return None

# from http://stackoverflow.com/questions/899067/how-should-i-verify-a-log-message-when-testing-python-code-under-nose
class MockLoggingHandler(logging.Handler):
    """ Mock logging handler to check for expected logs. """
    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self,*args,**kwargs)

    def emit(self,record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug':[],
            'info':[],
            'warninig':[],
            'error':[],
            'critical':[],
        }