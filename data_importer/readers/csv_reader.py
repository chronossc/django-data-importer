# coding: utf-8
import csv
from .base import BaseReader

class CSVReader(BaseReader):

    def __init__(self,f,**kwargs):
        self.delimiter = kwargs.pop('delimiter',';')
        super(CSVReader,self).__init__(f)



    def unload(self):
        """
        Close the input file and free resources, it matters for big files :)
        """
        if isinstance(self.source,file):
            self.source.close()
        else:
            self.source = None

        self.loaded = False

    def get_items(self):
        reader = csv.reader(self.source,delimiter=self.delimiter)
        self.headers = reader.next()
        for row in reader:
            if not row: continue
            yield self.get_item(row)

