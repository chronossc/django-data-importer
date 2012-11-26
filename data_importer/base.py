# coding: utf-8

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile
from django.utils.datastructures import SortedDict
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from data_importer.exceptions import UnknowSource
from data_importer.readers import *
import sys
import traceback
import logging

class FailedInStart(Exception):
    pass

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
        self.set_logger()
        self._load(import_file)
        self.reader = self._get_reader(reader,reader_kwargs)
        assert self._validate_class() is True # do not remove this line!!!!
        if settings.DEBUG:
            self.logger.setLevel(logging.DEBUG)
        else:self.logger.setLevel(logging.INFO)

    def _validate_class(self):
        """
        Somethings here is important, as sample we need fields :)
        """
        assert self.fields not in EMPTY_VALUES,_(u"You should set attribute fields in class!")
        assert self.reader is not None,_(u"Reader not loaded!")
        assert self.logger is not None,_(u"Logger not loaded!")

        return True

    def _load(self, source):
        """
        Load a file or a file path to self.import_file
        """
        try:
            if isinstance(source, file):
                self.import_file = source
            if isinstance(source,FieldFile):
                self.import_file = open(source.file.name, 'rb')
            if isinstance(source, basestring):
                self.import_file = open(source, 'rb')
        except Exception, err:
            raise UnknowSource(err)

        self.loaded = True

    def _get_reader(self,reader=None,reader_kwargs={}):
        """
        Initialize reader or choose one of existents based on extension of file.
        """
        try:
            if reader:
                return reader(self.import_file,**reader_kwargs)

            parts = self.import_file.name.rsplit('.',1)
            if len(parts) < 2:
                raise ValueError,_(u"Impossible to discover file extension! You should specify a reader from data_importer.readers.")
            if parts[-1].lower() not in READERS_X_EXTENSIONS:
                raise ValueError,_(u"Doesn't exist a relation between file extension and a reader. You should specify a reader from data_importer.readers or crete your own.")
            return READERS_X_EXTENSIONS[parts[-1].lower()](self.import_file,**reader_kwargs)
        except Exception:
            exc_info = sys.exc_info()
            self.logger.debug("\n".join(traceback.format_exception(*exc_info)))
            self.logger.critical(_("Something goes wrong when try to read the file!"))
            raise

    def set_logger(self):
        """
        Initialize the logger, I recommend that you not change this method ;)
        """
        try:
            logging.setLoggerClass(self.get_logger_class())
        except NotImplementedError:
            pass

        try:
            handlers = self.get_logger_handlers()
        except NotImplementedError:
            handlers = []
            logging.basicConfig(format=u'%(asctime)s :: %(levelname)s :: %(message)s')

        self.logger = logging.getLogger('%s_importer' % self.__class__.__name__)
        # remove handlers that can come with logger
        for h in self.logger.handlers:
            self.logger.removeHandler(h)
        self.logger.propagate = False

        # set defined handlers as defined in self.get_logger_handlers
        for h,hargs,hkwargs in handlers:
            self.logger.addHandler(h(*hargs,**hkwargs))

        if not self.logger.handlers:
            self.logger.handlers = self.logger.parent.handlers

        try:
            if settings.DEBUG:
                self.logger.setLevel(logging.DEBUG)
        except ImportError:
            pass

    def get_logger_class(self):
        """
        Supports a custom logger class that should be instantiated by set_logger.
        Read http://docs.python.org/library/logging.html#logging.setLoggerClass
        """
        raise NotImplementedError

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

    def _iter_clean_all(self):
        self.errors = SortedDict()
        for i,row in enumerate(self.reader,1):
            yield i,self._clean(i,row)

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

        if not any(_row.values()):
            self.logger.warning(u"Linha %s é vazia, foi ignorada." % i)
            return

        line_errors = SortedDict()
        row = _row.copy()
        row['_i'] = i

        def append_error(field,msg):
            if i not in self.errors:
                self.errors[i] = []
            if isinstance(msg,ValidationError):
                self.errors[i] = list(set(self.errors[i]+map(smart_unicode,msg.messages)))
                return map(smart_unicode,msg.messages)[0]
            else:
                self.errors[i] = list(set(self.errors[i] + [smart_unicode(msg)]))
                return smart_unicode(msg)

        # validate required fields first
        for field in self.required_fields:
            if row[field] in EMPTY_VALUES:
                if field not in line_errors:
                    line_errors[field] = [append_error(field,_(u"Field %s is required!") % field)]
                else:
                    line_errors[field].append(append_error(field,_(u"Field %s is required!") % field))
                continue
        # now validate each field
        for field in self.fields:

            if field in line_errors:
                continue
            if field not in row:
                row[field] = u''
            if hasattr(self,'clean_%s' % field):
                try:
                    val = getattr(self,'clean_%s' % field)(row[field],row.copy())
                    row[field] = val
                except ValidationError, msg:
                    if field not in line_errors:
                        line_errors[field] = [append_error(field,msg)]
                    else:
                        line_errors[field].append(append_error(field,msg))

        if line_errors:
            self.errors[i] = line_errors.copy()
            self._validation_results[i] = False
            for field,error in line_errors.items():
                for errmsg in error:
                    self.logger.error(_("Line %(line)s, field %(field)s: %(err)s") % {'line':i,'field':field,'err':errmsg})
            return False

        self._validation_results[i] = row
        return row

    def save_all_iter(self):
        return self.save_all(use_generator=True)

    def save_all(self,use_generator=False):
        try:
            if use_generator:
                def save_gen(self):
                    for i,row in self._iter_clean_all():
                        yield self.save(i,row)
                    try:
                        self.post_save_all()
                    except NotImplementedError:
                        pass
                return save_gen(self)
            else:
                rows = [self.save(i,row) for i,row in self._iter_clean_all()]
                try:
                    self.post_save_all()
                except NotImplementedError:
                    pass
                return rows
        except Exception as err:
            exc_info = sys.exc_info()
            self.logger.debug(self.logger.debug("\n".join(traceback.format_exception(*exc_info))))
            self.logger.critical(_("Process stoped with error %s: %s."),err.__class__.__name__, err)


    def save(self,i,row):
        """
        Save method should be customized to save data as user want.
        The default one just return row.
        """
        if row:
            self.logger.info(_(u"Line %s saved successfully"),i)
            return row

    def post_save_all(self):
        """
        # TODO: use signals
        Play here if you need to do something with importer after save_all runs.
        """
        raise NotImplementedError
