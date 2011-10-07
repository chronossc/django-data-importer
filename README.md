# Django Data Importer

Data importer was created with intention of be a good base to create importers that import anything to anywhere.
Data importer have support to custom file (may stream) readers, a interface with [Python Logging Library](http://docs.python.org/library/logging.html) that allow you to use custom logging handlers, support to data validation for each defined field of each line (very similar to Django Form Validation), support to required fields and finally a save method that you can customize to meet your needs.

It was idealized by https://github.com/ricobl/django-importer/ (I hope we merge projects) and special needs at work. Thx very much to [@ricobl](http://twitter.com/ricobl) wich created django-importer and to [@augustocmen](http://twitter.com/augustomen) that provided very nice tips for data importer development.

