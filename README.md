# Django Data Importer

Data importer was created with intention of be a good base to create importers that import anything to anywhere.
Data importer have support to custom file (may stream) readers, a interface with [Python Logging Library](http://docs.python.org/library/logging.html) that allow you to use custom logging handlers, support to data validation for each defined field of each line (very similar to Django Form Validation), support to required fields and finally a save method that you can customize to meet your needs.

It was idealized by https://github.com/ricobl/django-importer/ (I hope we merge projects) and special needs at work. Thx very much to [@ricobl](http://twitter.com/ricobl) wich created django-importer and to [@augustomen](http://twitter.com/augustomen) that provided very nice tips for data importer development.

# To the hurry people, a simple example with CSV text

This sample will use a CSV like the one bellow to demonstrate a very simple use of data_importer.

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
                                                                                                                                               
3. You
                                                                                                                        
                                                                                                                                               
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
        print result
        
```
