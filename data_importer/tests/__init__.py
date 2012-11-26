"""

"""
import os
import data_importer
from django.test import TestCase
from data_importer.tests.cpfcnpj import CPF
from data_importer.tests.importers import BaseImportWithFields, SimpleValidationsImporter, RequiredFieldValidationsImporter,\
    SimpleValidationsImporterDB, RequiredFieldValidationsImporterDB
from django.utils.datastructures import SortedDict
from data_importer.tests.mocks import MockLoggingHandler
from data_importer.handlers import DBLoggingHandler
from data_importer.tests.models import Error

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
        {'cpf': 96177843514, 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u'some data for field 5'},
        {'cpf': 87894839957, 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u''},
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
                self.assertEquals(self.f_data[i][k],line[k],
                    "Line %s, %s failed: %s != %s." % (i, k,
                        repr(self.f_data[i][k]), repr(line[k])))

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
        self.assertTrue(importer.is_valid(),u"BaseImporter isn't valid for CSV sheet.")
        del(importer)

    def test_before_clean__validation_results(self):
        """ attr __validation_results should be empty SortedDict """
        importer = SimpleValidationsImporter(self.files['csv_sheet'])
        self.assertEquals(SortedDict(),importer._validation_results)

    def test_before_clean_errors(self):
        """ attr errors should be empty SortedDict """
        importer = SimpleValidationsImporter(self.files['csv_sheet'])
        self.assertEquals(SortedDict(),importer.errors)

    def test_mock_log_instance(self):
        importer = SimpleValidationsImporter(self.files['csv_sheet'])
        self.assertTrue(isinstance(importer.logger.handlers[0],MockLoggingHandler))


    def test_mock_log_instance_handler(self):
        importer = SimpleValidationsImporter(self.files['csv_sheet'])
        self.assertTrue(isinstance(importer.logger.handlers[0],MockLoggingHandler))

    def test_mock_log_instance_handlers(self):
        """
        Each time we call set_logger only one instance of handlers should
        exist. We should assert that only one instance of each handlers is live
        """
        importer = SimpleValidationsImporter(self.files['csv_sheet'])
        instances = []
        for i in importer.logger.handlers:
            self.assertTrue(i.__class__.__name__ not in instances,u"More than one logger with same class found in importer.logger.handlers")
            instances.append(i.__class__.__name__)

class ImportersValidationsTests(TestCase):
    """
    This test will test other importers that should validate data.
    """
    def setUp(self):
        setUpClassData(self)

        self.data_invalid = [
            {'cpf': u'', 'field3': u'', 'field4': u'Emperor Palpatine: Soon the Rebellion will be crushed and young Skywalker will be one of us!', 'field5': u''},
            {'cpf': u'441.903.660-64', 'field3': u'Darth Vader: When I left you, I was but the learner. Now I am the master.', 'field4': u'some data for field 4', 'field5': u''},
            {'cpf': u'46177843514', 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u'some data for field 5'},
            {'cpf': u'87894839957', 'field3': u'Ben (Obi-Wan) Kenobi: The Force can have a strong influence on a weak mind.', 'field4': u'', 'field5': u''},
            {'cpf': u'933.331.456-34', 'field3': u'lines 3 and 5 have invalid cpfs, line 2 have null cpf', 'field4': u'', 'field5': u''},
        ]
        self.invalid_lines = {2: {'cpf': [u'Invalid CPF number.']}, 3: {'cpf': [u'Invalid CPF number.']}}
        self.logger_error_messages = [u"Line 2, field cpf: Invalid CPF number.", u"Line 3, field cpf: Invalid CPF number."]

    def test_simple_false_validation(self):
        importer = SimpleValidationsImporter(self.files['csv_invalid_cpf_sheet'])
        self.assertTrue(not importer.is_valid(),u"Should return False to is_valid()")

    def test_invalid_lines(self):
        importer = SimpleValidationsImporter(self.files['csv_invalid_cpf_sheet'])
        self.assertTrue(not importer.is_valid(),u"Should return False to is_valid()")
        for i in self.invalid_lines:
            self.assertEquals(False,importer._validation_results[i])

    def test_invalid_errors(self):
        importer = SimpleValidationsImporter(self.files['csv_invalid_cpf_sheet'])
        self.assertTrue(not importer.is_valid(),u"Should return False to is_valid()")
        self.assertNotEquals(SortedDict(),importer.errors) # importer.errors shouldn't be empty
        for i in importer.errors:
            self.assertEquals(True,i in self.invalid_lines)
            for k,v in importer.errors[i].items():
                self.assertEquals(True,k in self.invalid_lines[i])
                self.assertEquals(self.invalid_lines[i][k],v)

    def test_invalid_errors_in_logging(self):
        importer = SimpleValidationsImporter(self.files['csv_invalid_cpf_sheet'])
        self.assertTrue(not importer.is_valid(),u"Should return False to is_valid()")
        self.assertTrue(importer.logger,u"Logger isn't set")
        self.assertEquals(self.logger_error_messages,importer.logger.handlers[0].messages['error'])

    def test_invalid_errors_in_logging_to_DB(self):
        importer = SimpleValidationsImporterDB(self.files['csv_invalid_cpf_sheet'])

        self.assertEquals([],list(Error.objects.all())) # apply list to queryset
        self.assertTrue(not importer.is_valid(),u"Should return False to is_valid()")
        self.assertTrue(importer.logger,u"Logger isn't set")
        self.assertTrue(isinstance(importer.logger.handlers[0],DBLoggingHandler),u"Logger handler isn't DBLoggingHandler")

        errors = Error.objects.all()
        self.assertTrue(u"SimpleValidationsImporterDB_importer :: error :: Line 2, field cpf: Invalid CPF number." in \
            str(errors[0]),u"Weird string for this test, check loggers.")
        self.assertTrue(u"SimpleValidationsImporterDB_importer :: error :: Line 3, field cpf: Invalid CPF number." in \
            str(errors[1]),u"Weird string for this test, check loggers.")

    def test_invalid_required_field(self):
        # invalid lines for RequiredFieldValidationsImporter includes line 1 :)
        invalid_lines = self.invalid_lines.copy()
        invalid_lines.update({1: {'field3': [u'Field field3 is required!'], 'cpf': [u'Field cpf is required!']}})

        importer = RequiredFieldValidationsImporter(self.files['csv_invalid_cpf_sheet'])
        self.assertEquals([],list(Error.objects.all())) # apply list to queryset
        self.assertTrue(not importer.is_valid(),u"Should return False to is_valid()")

        for i in importer.errors:
            self.assertEquals(True,i in invalid_lines)
            for k,v in importer.errors[i].items():
                self.assertEquals(True,k in invalid_lines[i])
                self.assertEquals(invalid_lines[i][k],v)

    def test_invalid_required_field_DB(self):
        importer = RequiredFieldValidationsImporterDB(self.files['csv_invalid_cpf_sheet'])

        self.assertEquals([],list(Error.objects.all())) # apply list to queryset
        self.assertTrue(not importer.is_valid(),u"Should return False to is_valid()")
        self.assertTrue(importer.logger,u"Logger isn't set")
        self.assertTrue(isinstance(importer.logger.handlers[0],DBLoggingHandler),u"Logger handler isn't DBLoggingHandler")

        errors = Error.objects.all()

        self.assertTrue(u"RequiredFieldValidationsImporterDB_importer :: error :: Line 1, field cpf: Field cpf is required!" in \
            str(errors[0]),u"Weird string for this test, check loggers.")
        self.assertTrue(u"RequiredFieldValidationsImporterDB_importer :: error :: Line 1, field field3: Field field3 is required!" in \
            str(errors[1]),u"Weird string for this test, check loggers.")
        self.assertTrue(u"RequiredFieldValidationsImporterDB_importer :: error :: Line 2, field cpf: Invalid CPF number." in \
            str(errors[2]),u"Weird string for this test, check loggers.")
        self.assertTrue(u"RequiredFieldValidationsImporterDB_importer :: error :: Line 3, field cpf: Invalid CPF number." in \
            str(errors[3]),u"Weird string for this test, check loggers.")

    def test_save(self):
        # test save against invalid lines
        invalid_lines = self.invalid_lines.copy()
        invalid_lines.update({1: {'field3': [u'Field field3 is required!'], 'cpf': [u'Field cpf is required!']}})
        importer = RequiredFieldValidationsImporterDB(self.files['csv_invalid_cpf_sheet'])
        results = [i for i in importer.save_all_iter()]
        for i,know_data in enumerate(self.data_invalid):
            data = results[i]
            if not data and i+1 in invalid_lines: # dict data starts from 1
                self.assertEquals(data,None)
            else:
                for k,v in know_data.items():
                    # RequiredFieldValidationsImporterDB should return field
                    # CPF as instance of data_importer.tests.cpfcnpj.CPF class,
                    # so we make cpf a instance before comparation
                    if k == 'cpf':
                        v = CPF(v)
                    self.assertEquals(True,k in data)
                    self.assertEquals(data[k],v)
