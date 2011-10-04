"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from sample.cpfcnpj import CPF, CPFGenerator

class CPFTest(TestCase):
    def test_valid_cpf(self):
        cpf = '31506331840'
        self.assertEquals('315.063.318-40',str(CPF(cpf)))

