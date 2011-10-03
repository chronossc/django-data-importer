# coding: utf-8
from django.utils.datastructures import SortedDict
from django.utils.encoding import smart_unicode

class BaseReader(object):

    loaded = False
    source = None
    headers = None

    def __init__(self,f):
        """
        init receive f as a file object
        """
        self._load(f)

    def __iter__(self):
        return self.get_items()

    def _load(self, source):
        """
        Load a file or a file path to self.source.
        """
        try:
            if isinstance(source, file):
                self.source = source
            if isinstance(source, basestring):
                self.source = open(source, 'rb')
        except Exception, err:
            raise UnknowSource(err)

        self.loaded = True

    def unload(self):
        """
        Close the input file and free resources, it matters for big files :)
        """
        if isinstance(self.source,file):
            self.source.close()
        else:
            self.source = None

        self.loaded = False

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

    def get_items(self):
        """
        Iterator do read the rows of file. Should return a dict with fields
        name and values. get_items should set headers too.
        """
        raise NotImplementedError


