# coding: utf-8
from django.utils.datastructures import SortedDict
from django.utils.encoding import smart_unicode

class BaseReader(object):

    def __init__(self,f):
        """
        init receive f as a file object
        """
        self.loaded = False
        self.source = None
        self._reader = None
        self._headers = None
        self.__load(f)

    def __iter__(self):
        return self.get_items()

    def __load(self, source):
        """
        Load a file or a file path to self.source.
        Don't touch in this method, some assertions here is really important
        """
        try:
            if isinstance(source, file):
                self.source = source
            if isinstance(source, basestring):
                self.source = open(source, 'rb')
        except Exception, err:
            raise UnknowSource(err)

        self.loaded = True
        self.set_reader()
        assert self._reader is not None
        assert self.headers is not None # call self.get_headers

    def unload(self):
        """
        Close the input file and free resources, it matters for big files :)
        """
        if isinstance(self.source,file):
            self.source.close()
        else:
            self.source = None

        self.loaded = False

    def set_reader(self):
        """
        This method will start file reader if necessary because normally each
        file type can have a existent reader in python and BaseReader can't
        know it.
        This method is called in self.__load after source is read and should set
        self._reader. self.get_items and self.get_header should read self._reader.
        """
        self._reader = self.source

    def get_value(self,item,field):
        """
        Receive item and field and should return value of field in item. Can be
        customized to handle various types.
        """
        val = item.get(field.encode('utf-8'), None)
        if val is not None:
            return smart_unicode(val)
        return val

    def get_item(self,row):
        """
        Given a header and a row return a sorted dict
        """ 
        d = SortedDict(zip(self.headers,map(smart_unicode,row)))
        # since zip cut tuple to smaller sequence, if we get incomplete
        # lines in file this for over headers put it on row dict
        for k in self.headers:
            if k not in d:
                d[k]=u''
        d.keyOrder = self.headers
        return d

    def get_headers(self):
        """
        Should set self._headers and should run only one time.

        Since header normally is first line of the file, we get the first one
        here, but we can't know format that reader should be read, so we just
        do a next on reader.

        This method runs as headers property
        """
        if not self._headers:
            self._headers = self._reader.next()
        return self._headers
    
    headers = property(get_headers)

    def get_items(self):
        """
        Iterator do read the rows of file. Should return a dict with fields
        name and values. get_items should set headers too.
        """
        raise NotImplementedError


