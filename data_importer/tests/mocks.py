# coding: utf-8

import logging

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
            'warning':[],
            'error':[],
            'critical':[],
        }