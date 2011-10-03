"""

"""
import os
from django.test import TestCase
#from data_importer.readers import BaseReader, CSVReader
import data_importer


class ReaderTest(TestCase):
    """
    Test various headers against already know data.
    If you will write a new reader, use this csv data as base:

    cpf;field3;field4;field5
    437.692.351-69;;Emperor Palpatine: Soon the Rebellion will be crushed and young Skywalker will be one of us!
    541.903.660-64;Darth Vader: When I left you, I was but the learner. Now I am the master.;some data for field 4
    96177843514;Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.;;some data for field 5
    87894839957;Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.
    933.331.456-34;Princess Leia: Aren't you a little short for a stormtrooper?

    This file have blank value and field not filleds and reader should handle it.
    """
    
    def setUp(self):
        """
        S
        """
        mod_dir = os.path.realpath(os.path.dirname(data_importer.tests.__file__))
        self.files = {
            'csv_sheet': os.path.join(mod_dir,'fixtures','csv_sheet.csv')
        }

        self.f_headers = ['cpf','field3','field4','field5']
        self.f_data = [
            {'cpf': u'437.692.351-69', 'field3': u'', 'field4': u'Emperor Palpatine: Soon the Rebellion will be crushed and young Skywalker will be one of us!', 'field5': u''},
            {'cpf': u'541.903.660-64', 'field3': u'Darth Vader: When I left you, I was but the learner. Now I am the master.', 'field4': u'some data for field 4', 'field5': u''},
            {'cpf': u'96177843514', 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u'some data for field 5'},
            {'cpf': u'87894839957', 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u''},
            {'cpf': u'933.331.456-34', 'field3': u"Princess Leia: Aren't you a little short for a stormtrooper?", 'field4': u'', 'field5': u''},
        ]

    def compare_lines(self,lines):
        for i,line in enumerate(lines):
            for k in line:
                self.assertEquals(self.f_data[i][k],line[k])

    def test_base_reader_init(self):
        self.assertTrue(os.path.isfile(self.files['csv_sheet']),u"file for basereader test not exists")
        reader = data_importer.readers.BaseReader(self.files['csv_sheet'])
        self.assertEquals(open(self.files['csv_sheet'],'rb').read(),reader.source.read())

    def test_csv_reader(self):
        """
        Compare data return by CSVReader from csv_sheet.csv file to know data
        """
        reader = data_importer.readers.CSVReader(self.files['csv_sheet'])
        [line for line in reader]
        self.assertEquals(self.f_headers,reader.headers)

    def test_csv_lines(self):
        reader = data_importer.readers.CSVReader(self.files['csv_sheet'])
        self.compare_lines([line for line in reader])
        

