from django.db import models

# Create your models here.

class TheModel(models.Model):
    cpf = models.CharField(max_length=11)
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)
    field3 = models.CharField(max_length=100)
    field4 = models.CharField(max_length=100)
    field5 = models.CharField(max_length=100)
    field6 = models.CharField(max_length=100)
    field7 = models.CharField(max_length=100)
    field8 = models.CharField(max_length=100)
    field9 = models.CharField(max_length=100)
    field10 = models.CharField(max_length=100)

    def __unicode__(self):
        return self.cpf

