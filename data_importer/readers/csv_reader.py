# coding: utf-8
import csv
from .base import BaseReader

class CSVReader(BaseReader):

    def __init__(self,f,**kwargs):
        self.delimiter = kwargs.pop('delimiter',';')
        super(CSVReader,self).__init__(f)

    def set_reader(self):
        self._reader = csv.reader(self._source,delimiter=self.delimiter)

    def get_value(self,item,**kwargs):
        try:
            int(item)
        except:
            pass
        else:
            return int(item)
        return item

    def get_items(self):
        for row in self._reader:
            if not row: continue # invalid lines are ignored
            yield self.get_item([self.get_value(i) for i in row])
