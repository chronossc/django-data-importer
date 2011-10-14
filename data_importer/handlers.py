# coding: utf-8

import logging
from logging import StreamHandler

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

# define a generic database logger handler.
class DBLoggingHandler(logging.Handler):
    # based on https://github.com/dcramer/django-db-log/blob/master/djangodblog/handlers.py
    def __init__(self,*args,**kwargs):
        self.model = kwargs.pop('model')
        assert hasattr(self.model.objects,'create_from_record') is True
        logging.Handler.__init__(self,*args,**kwargs)

    def emit(self,record):
        return self.model.objects.create_from_record(record)
        

