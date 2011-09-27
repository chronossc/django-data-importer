# coding: utf-8
import csv
from .base import Reader

class CSVReader(Reader):

    def __init__(self,f,delimiter=';'):
        self.delimiter = delimiter
        super(CSVReader,self).__init__(f)

    def get_items(self):
        reader = csv.reader(self.source,delimiter=self.delimiter)
        header = reader.next()
        for row in reader:
            if not row: continue
            yield self.get_item(header,row)

