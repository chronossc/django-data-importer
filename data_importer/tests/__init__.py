"""

"""
import os
from django.test import TestCase
#from data_importer.readers import BaseReader, CSVReader
import data_importer


class ReaderTest(TestCase):
    
    def setUp(self):
        mod_dir = os.path.realpath(os.path.dirname(data_importer.tests.__file__))
        self.files = {
            'csv_sheet': os.path.join(mod_dir,'fixtures','csv_sheet.csv')
        }

    def test_base_reader_init(self):
        self.assertTrue(os.path.isfile(self.files['csv_sheet']),u"file for basereader test not exists")
        reader = data_importer.readers.BaseReader(self.files['csv_sheet'])
        self.assertEquals(open(self.files['csv_sheet'],'rb').read(),reader.source.read())

    def test_csv_reader(self):
        """
        Compare data return by CSVReader from csv_sheet.csv file to know data
        """
        # csv_sheet.csv was created in bash using fortunes and generated cpfs.
        # since we know csv_sheet output we compare CSVReader output with it.
        headers = ['cpf','field3','field4','field5']
        data = [
            {'cpf': u'437.692.351-69', 'field3': u'', 'field4': u'Emperor Palpatine: Soon the Rebellion will be crushed and young Skywalker will be one of us!', 'field5': u''},
            {'cpf': u'541.903.660-64', 'field3': u'Darth Vader: When I left you, I was but the learner. Now I am the master.', 'field4': u'some data for field 4', 'field5': u''},
            {'cpf': u'96177843514', 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u'some data for field 5'},
            {'cpf': u'87894839957', 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u''},
            {'cpf': u'933.331.456-34', 'field3': u"Princess Leia: Aren't you a little short for a stormtrooper?", 'field4': u'', 'field5': u''},
        ]

        reader = data_importer.readers.CSVReader(self.files['csv_sheet'])
        lines = [line for line in reader]

        self.assertEquals(headers,reader.headers)
        for i,line in enumerate(lines):
            for k in line:
                self.assertEquals(data[i][k],line[k])
