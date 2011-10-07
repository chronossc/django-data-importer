# Django Data Importer

Data importer was created with intention of be a good base to create importers that import anything to anywhere.
Data importer have support to custom file (may stream) readers, a interface with [Python Logging Library](http://docs.python.org/library/logging.html) that allow you to use custom logging handlers, support to data validation for each defined field of each line (very similar to Django Form Validation), support to required fields and finally a save method that you can customize to meet your needs.

It was idealized by https://github.com/ricobl/django-importer/ (I hope we merge projects) and special needs at work. Thx very much to [@ricobl](http://twitter.com/ricobl) wich created django-importer and to [@augustomen](http://twitter.com/augustomen) that provided very nice tips for data importer development.

# Basic usage

This sample will use a CSV to demonstrate a very simple use of data_importer.

##1. The CSV contents:

```csv
email;field1;field2;field3
mail1@devwithpassion.com;django;data;importer
mail2@devwithpassion.com;web2py;no;data_importer
```

(To-do: csv module accept text instead a file too and I'll support it soon)

##2. Create your importer

Import BaseImporter and extend it with your class.

```python
from data_importer import BaseImporter

class Importer1(BaseImporter):
    fields = ['email','field1','field2','field3']
    required_fields = ['email'] # optional

    def clean_email(self,val):
        from django.core.validators import validate_email
        validate_email(val)
        # validate_email raises ValidationError if invalid

```
### Important (and basic) things!

1. You should define fields that you will have on your files, and first line of files should be headers. required_fields is optional.

2. If you wanna to validate your fields you should implement methods in importer like clean_<field_name>. The method will receive a attr **val** and should return cleaned value or raise ValidationError.
                                                                                                                                               
3. You **SHOULD** write a save method in Importer. The save method receive i and row, where i is number of line, and row is a dict with validated row. Otherwise you will receive only a dict with data.
                                                                                                                        
                                                                                                                                               
##3. Instantiate importer and than save

Create a new instance of importer with the file:

```python
importer = Importer1('path/to/csv_file.csv')
```

And than, just call **save_all** or **save_all_iter**:

```python
results = importer.save_all()

#or
for i,result in enumerate(importer.save_all_iter(),1):
    # result can be False or a dict with row data
    if result is False:
        print u"Line %s: Invalid entry." % i
    else:
        print result # {'email': u'mail1@devwithpassion.com', 'field1': u'django', 'field2': u'data', 'field3': u'importer'}
        
```

# Some cool logging stuff

As you see it's very easy to start using data_importer. In save method you can write something that save to your model and be very happy.

But, many times people need a log of things that happens, and data_importer comes with a fun DBLoggingHandler.
**DBLoggingHandler should be instantiated with model that you will save logs and model manager should have a method called create_from_record**. To assign handlers to importer.logger logging instance you should put a method called **get_logger_handlers** that returns a list of tuples with Handler, args to handler and kwargs to handler.

See the example:

```python
from django.db import models
from data_importer import BaseImporter

# first the Error model
LOG_LEVELS = (
    (logging.INFO, 'info'),
    (logging.WARNING, 'warning'),
    (logging.DEBUG, 'debug'),
    (logging.ERROR, 'error'),
    (logging.FATAL, 'fatal'),
)

class ErrorManager(models.Manager):
    def create_from_record(self,record):
        entry = Error(
            logger=record.name,
            msg=record.getMessage(),
            levelno=record.levelno
        )
        entry.save()
        return entry

class Error(models.Model):
    logger = models.CharField(max_length=100)
    msg = models.TextField()
    levelno = models.IntegerField(choices=LOG_LEVELS)
    created = models.DateTimeField(auto_now_add=True)
    

# now my importer
class Importer2(BaseImporter):
    fields = ['email','field1','field2','field3']
    
    def get_logger_handlers(self):
        # A internal method will initiate DBLoggingHandler, so you send args and kwargs.
        # With this way you can provide many handlers as you want :)
        return [(DBLoggingHandler,(),{'model':Error})]

    def clean_email(self,val):
        from django.core.validators import validate_email
        validate_email(val)
        # validate_email raises ValidationError if invalid

# than run
importer = Importer1(csv_file)
importer.save_all()

```

BaseImporter set self.logger as a logging instance with name of class, so any call to self.logger.<debug|info|warning|error|critical> method will log to DBLoggingHandler now.

You can find a better model for DBLogging in tests :).

# Docs, Developing and testing data_importer

Since I started right now I don't have much more doc than this README, but I'll make a full doc of internal methods until end of Oct/2011.

To test the project you need to go to sampleproject and run ./manage.py test data_importer. For now I guess I tested all code, but I'll put code coverate stats soon.

If you like the project, plz, contact me at philipe.rp@gmail.com (gtalk and email) and help me improve it.

Here is some stuff that I like to put:

* Better logging support on various methods of BaseImporter
* Add a SentryLogginHandler to data_importer
* Add support to more file formats, like openoffice ones, pure xmls, JSON and any other type adding readers to it.
* Add support to stream in readers, so user can put text instead a file and maybe avoid disk I/O.
* Add support to gettext and internatiolization
* Add a ModelBaseReader class that read fields from a Model and save directly to a model, using model field validations.
* Make data_importer works without Django, so anyone in Python world can use it.

# TIP: READ THE TESTS, THEY COVER A LOT OF WAYS TO USE DATA IMPORTER :)

