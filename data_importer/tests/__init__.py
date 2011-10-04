"""

"""
import os
import data_importer
from django.test import TestCase
from importers import BaseImportWithFields, SimpleValidationsImporter, RequiredFieldValidationsImporter

def setUpClassData(klass):
    """
    This method should receive one test class and setup common data used over all tests classes.

    If you will write a new reader, use this csv data as base:

    cpf;field3;field4;field5
    437.692.351-69;;Emperor Palpatine: Soon the Rebellion will be crushed and young Skywalker will be one of us!
    541.903.660-64;Darth Vader: When I left you, I was but the learner. Now I am the master.;some data for field 4

    96177843514;Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.;;some data for field 5
    87894839957;Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.
    933.331.456-34;Princess Leia: Aren't you a little short for a stormtrooper?

    This file have blank value and field not filleds and reader should handle it. Also a blank line that should be ignorated.
    """
    mod_dir = os.path.realpath(os.path.dirname(data_importer.tests.__file__))
    klass.files = {
        'csv_invalid_cpf_sheet': os.path.join(mod_dir,'fixtures','csv_invalid_cpf_sheet.csv'), # used to get validation errors
        'csv_sheet': os.path.join(mod_dir,'fixtures','csv_sheet.csv'),
        'xls_sheet': os.path.join(mod_dir,'fixtures','xls_sheet.xls'),
        'xlsx_sheet': os.path.join(mod_dir,'fixtures','xlsx_sheet.xlsx'),           
    }

    klass.f_headers = ['cpf','field3','field4','field5']
    klass.f_data = [
        {'cpf': u'437.692.351-69', 'field3': u'', 'field4': u'Emperor Palpatine: Soon the Rebellion will be crushed and young Skywalker will be one of us!', 'field5': u''},
        {'cpf': u'541.903.660-64', 'field3': u'Darth Vader: When I left you, I was but the learner. Now I am the master.', 'field4': u'some data for field 4', 'field5': u''},
        {'cpf': u'96177843514', 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u'some data for field 5'},
        {'cpf': u'87894839957', 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u''},
        {'cpf': u'933.331.456-34', 'field3': u"Princess Leia: Aren't you a little short for a stormtrooper?", 'field4': u'', 'field5': u''},
    ]

class ReaderTest(TestCase):
    """
    Test various readers results against already know data.

    """
    
    def setUp(self):
        setUpClassData(self)

    def compare_lines(self,lines):
        for i,line in enumerate(lines):
            for k in line:
                self.assertEquals(self.f_data[i][k],line[k])

    def test_base_reader_init(self):
        self.assertTrue(os.path.isfile(self.files['csv_sheet']),u"file for basereader test not exists")
        reader = data_importer.readers.BaseReader(self.files['csv_sheet'])
        f = open(self.files['csv_sheet'],'rb').read()
        self.assertEquals(f,reader._source.read())

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

    def test_xls_reader(self):
        """
        Compare data return by CSVReader from csv_sheet.csv file to know data
        """
        reader = data_importer.readers.XLSReader(self.files['xls_sheet'])
        [line for line in reader]
        self.assertEquals(self.f_headers,reader.headers)

    def test_xls_lines(self):
        reader = data_importer.readers.XLSReader(self.files['xls_sheet'])
        self.compare_lines([line for line in reader])

    def test_xlsx_reader(self):
        """
        Compare data return by CSVReader from csv_sheet.csv file to know data
        """
        reader = data_importer.readers.XLSXReader(self.files['xlsx_sheet'])
        [line for line in reader]
        self.assertEquals(self.f_headers,reader.headers)

    def test_xlsx_lines(self):
        reader = data_importer.readers.XLSXReader(self.files['xlsx_sheet'])
        self.compare_lines([line for line in reader])

class BaseImporterTests(TestCase):

    def setUp(self):
        setUpClassData(self)

    def test_baseauto_reader_select_csv(self):
        importer = BaseImportWithFields(self.files['csv_sheet'])
        self.assertTrue(isinstance(importer.reader,data_importer.readers.CSVReader),u"Auto selected reader for CSV isn't instance of CSVReader")
        del(importer)

    def test_baseauto_reader_select_xls(self):
        importer = BaseImportWithFields(self.files['xls_sheet'])
        self.assertTrue(isinstance(importer.reader,data_importer.readers.XLSReader),u"Auto selected reader for XLS isn't instance of XLSReader")
        del(importer)

    def test_baseauto_reader_select_xlsx(self):
        importer = BaseImportWithFields(self.files['xlsx_sheet'])
        self.assertTrue(isinstance(importer.reader,data_importer.readers.XLSXReader),u"Auto selected reader for XLSX isn't instance of XLSXReader")
        del(importer)

    def test_base_importer_validation(self):
        importer = BaseImportWithFields(self.files['csv_sheet'])
        print id(importer)
        self.assertTrue(importer.is_valid(),u"BaseImporter isn't valid for CSV sheet.")
        del(importer)

class ImportersTests(TestCase):
    """
    This test will test other importers that should validate data.
    """
    def setUp(self):
        setUpClassData(self)
 
    def test_simple_validation(self):
        importer = SimpleValidationsImporter(self.files['csv_invalid_cpf_sheet'])
        print id(importer)
        self.assertTrue(not importer._validation_results,u"How by the hell _validation_results is filled with no validation called!?")
        self.assertTrue(not importer.errors,u"How by the hell errors is filled with no validation called!?")
        self.assertTrue(not importer.is_valid(),u"Should return False to is_valid()")
        del(importer)