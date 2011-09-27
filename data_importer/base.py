# coding: utf-8
from django.conf import settings
from .readers import *
import logging


READERS_X_EXTENSIONS = {
    'csv': CSVReader,
}

class BaseImporter(object):

    fields = []
    reader = None
    loaded = False

    def __init__(self,import_file,reader=None,reader_kwargs={}):
        self._load(import_file)
        self.reader = self._get_reader(reader,reader_kwargs)
        self.set_logger()

    def _load(self, source):
        """
        Load a file or a file path to self.import_file
        """
        try:
            if isinstance(source, file):
                self.import_file = f
            if isinstance(source, basestring):
                self.import_file = open(source, 'rb')
        except Exception, err:
            raise UnknowSource(err)

        self.loaded = True

    def _get_reader(self,reader=None,reader_kwargs={}):
        """
        Initialize reader or choose one of existents based on extension of file.
        """
        if reader:
            return reader(self.import_file,**reader_kwargs)

        parts = self.import_file.name.rsplit('.',1)
        if len(parts) < 2:
            raise ValueError,u"Impossible to discover file extension! You should specify a reader from data_importer.readers."
        if parts[-1].lower() not in READERS_X_EXTENSIONS:
            raise ValueError,u"Doesn't exist a relation between file extension and a reader. You should specify a reader from data_importer.readers or crete your own."
        return READERS_X_EXTENSIONS[parts[-1].lower()](self.import_file,**reader_kwargs)

    def set_logger(self):
        self.logger = logging.getLogger()
        self.logger.propagate = False
        try:
            if settings.DEBUG:
                self.logger.setLevel(logging.DEBUG)
        except ImportError:
            pass
        try:
            for h,hargs,hkwargs in self.get_logger_handlers():
                print h,hargs,hkwargs
                self.logger.addHandler(h(*hargs,**hkwargs))
        except NotImplementedError:
            logging.basicConfig(format=u'%(asctime)s :: %(levelname)s :: %(message)s')


    def get_logger_handlers(self):
        """
        should return a list of logger handlers and args and kwargs:
        ( (StreamHandler,(),{}), (FileHandler,('/home/felipe/logs/import.log',),{}),...)
        """
        raise NotImplementedError

    def run(self):
        for i,row in enumerate(self.reader,1):
            self.clean(row)
            self.logger.info(u"Line %s: %s" % (i,row))
