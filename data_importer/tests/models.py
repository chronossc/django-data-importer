# coding: utf-8
from django.db import models
import logging

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
            levelno=record.levelno,
            pathname=record.pathname,
            funcname=record.funcName,
            lineno=record.lineno
        )
        entry.save()
        return entry

class Error(models.Model):
    logger = models.CharField(max_length=100)
    msg = models.TextField()
    levelno = models.IntegerField(choices=LOG_LEVELS)
    pathname = models.TextField() # cause can be greater than 256 chars
    funcname = models.CharField(max_length=100)
    lineno = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    objects = ErrorManager()

    def __unicode__(self):
        return u"%s :: %s :: %s :: %s" % (
            self.created,
            self.logger,
            self.get_levelno_display(),
            self.msg
        )