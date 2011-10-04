# coding: utf-8
from django.conf import settings
from .readers import *
from django.utils.datastructures import SortedDict
from django.utils.encoding import smart_unicode
from django.core.exceptions import ValidationError
import logging
import ipdb

READERS_X_EXTENSIONS = {
    'csv': CSVReader,
    'xls': XLSReader,
    'xlsx': XLSXReader,
}

# from django.core.validators.EMPTY_VALUES
EMPTY_VALUES = (None, '', [], (), {})

class BaseImporter(object):

    fields = []
    required_fields = []
    reader = None
    loaded = False
    errors = SortedDict() # {lineNum:list(set([error1,error2])),...}
    
    def __init__(self,import_file,reader=None,reader_kwargs={}):
        self._validation_results = SortedDict()
        self._load(import_file)
        self.reader = self._get_reader(reader,reader_kwargs)
        self.set_logger()
        assert self._validate_class() is True # do not remove this line!!!!
    
    def _validate_class(self):
        """
        Somethings here is important, as sample we need fields :)
        """
        assert self.fields not in EMPTY_VALUES,u"You should set attribute fields in class!"
        assert self.reader is not None,u"Reader not loaded!"
        assert self.logger is not None,u"Logger not loaded!"

        return True

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

    def is_valid(self):
        if not self._validation_results:
            self._clean_all()
        return not self.errors

    def _clean_all(self):
        self.errors = SortedDict()
        for i,row in enumerate(self.reader,1):
            self._clean(i,row)

    def _clean(self,i,_row):
        """
        Walk over all fields in a row and validate it. Validations will be cached.

        This method will call self.clean_<fieldname> with value as parameter.
        Method self.clean_<fieldname> should return correct value. Ther is
        no limitation to self.clean_<fieldname> value so you can return
        anything you need to work.

        This method calls self.logger.error() to log errors, so if you set a
        database logger handler errors will be saved on db.

        Return the row if validated, else None

        DON'T CALL THIS METHOD DIRECTLY!!
        This method should be called by self._clean_all
        
        """
        if i in self._validation_results:
            return self._validation_results[i]

        line_errors = {}
        row = _row.copy()
        def append_error(field,msg):
            if i not in self.errors:
                self.errors[i] = []
            msg
            self.errors[i] = list(set(self.errors[i]+[smart_unicode(msg)]))
            return smart_unicode(msg)

        # validate required fields first
        for field in self.required_fields:
            if row[field] in EMPTY_VALUES:
                line_errors[field] = append_error(field,u"Field %s is required!" % field)
                continue

        # now validate each field
        for field in self.fields:
            if field in line_errors:
                continue
            if hasattr(self,'clean_%s' % field):
                try:
                    val = getattr(self,'clean_%s' % field)(row[field])
                    row[field] = val
                except ValidationError, msg:
                    line_errors[field] = append_error(field,msg)

        if line_errors:
            self.errors[i] = line_errors.copy()
            self._validation_results[i] = False
            for field,error in line_errors.items():
                self.logger.error("Line %s, field %s: %s",i,field,error)
            return False
        self._validation_results[i] = row
        return row