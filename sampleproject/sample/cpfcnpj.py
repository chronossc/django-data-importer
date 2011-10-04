# -*- coding: utf-8 -*-

import re, math
from random import randint
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

# -------------------------------------------------
# Based in http://www.python.org.br/wiki/VerificadorDeCnpj
# This code was created for a path to django that lives in https://github.com/chronossc/django/blob/ticket13473/django/contrib/localflavor/br/br_cpfcnpj.py
# 
class CNPJ(object):
    """
    This class that represents a CNPJ number.
    CNPJ is National Registry of Corporations in Brazil.
    A CPF number is compounded by XX.XXX.XXX/XXXX-VD where:
      - First 8 digits is company id
      - The 4 digits after '/' is number of filial of company
      - Last two digits are verification digits

    >>> x=CNPJGenerator()
    >>> x
    '58364950000770'
    >>> CNPJ(x)
    CNPJ('58364950000770')
    >>> CNPJ(x).single
    u'58364950000770'
    >>> str(CNPJ(x))
    '58.364.950/0007-70'
    """

    error_messages = {
        'invalid': _(u"Invalid CNPJ number."),
        'max_digits': _(u"CNPJ requires at most 14 digits or 18 characters."),
        'digits_only': _(u"CNPJ requires only numbers, allow '.', '/' and '-' for long format."),
    }
    
    def __init__(self, cnpj):
        
        # transform list or int or long in a string
        if type(cnpj) in (int,long):
            cnpj = u"%s" % cnpj
        if type(cnpj) in (list,tuple):
            cnpj= u''.join([str(x) for x in cnpj])

        try:
            basestring
        except:
            basestring = (str, unicode)
        # only numbers = 14, numbers with '.', '/' and '-' = 18
        if len(cnpj) not in (14,18):
            raise ValueError(self.error_messages['max_digits'])

        if isinstance(cnpj, basestring):
            # remove characters
            cnpj = cnpj.replace(".", "")
            cnpj = cnpj.replace("-", "")
            cnpj = cnpj.replace("/", "")

            # and check if is digit
            if not cnpj.isdigit():
                raise ValueError(self.error_messages['digits_only'])

        # turn into a list of integers
        self.cnpj = map(int, cnpj)

        # validate number and validation digits
        if not self.is_valid:
            raise ValueError(self.error_messages['invalid'])

    def __getitem__(self, index):
        """
        Returns digit at index in CNPJ

        >>> a = CNPJ('11222333000181')
        >>> a[9] == '0'
        True
        >>> a[10] == '0'
        True
        >>> a[9] == 0
        False
        >>> a[10] == 0
        False

        """
        return str(self.cnpj[index])

    def __repr__(self):
        return "CNPJ('%s')" % ''.join([str(x) for x in self.cnpj])

    def __eq__(self, other):
        """
        >>> a = CNPJ('11222333000181')
        >>> b = CNPJ('11.222.333/0001-81')
        >>> c = CNPJ([1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 1, 8, 2])
        >>> a == b
        True
        >>> a != c
        True
        >>> b != c
        True
        """
        if isinstance(other, CNPJ):
            return self.cnpj == other.cnpj
        return False

    def __unicode__(self): 
        """
        Return CNPJ in long format, with '.', '/' and '.'. For simple format
        use CNPJ(...).single property/method

        >>> a = CNPJ('11222333000181')
        >>> str(a)
        u'11.222.333/0001-81'

        """
        d = ((2, "."), (6, "."), (10, "/"), (15, "-"))
        s = map(str, self.cnpj)
        
        for i, v in d:
            s.insert(i, v)
        
        r = ''.join(s)
        
        return r
    
    def __str__(self):
        return self.__unicode__()

    def __len__(self):
        return len(self.cnpj)

    @property
    def is_valid(self):
        """
        Validates CNPJ with first 8 digits + filial digits and validation
        digits.
        This method is used in __init__ to validate number.
        """

        # get company id + filial id (first 12 digits)
        cnpj = self.cnpj[:12]
        
        # and following rules we stabilish some weight to multiply
        def weightlist(s=12):
            x = (range(2,10)*2)[:s]
            x.reverse()
            return x
        
        # while cnpj isn't complete
        while len(cnpj) < 14:

            # run trought numbers (x) mutiplying by weight (y) and then get
            # sum of rest of division by 11 as interger
            # (we have more than 9 digits so isn't simple as make calcs for CPF)
            r = int(sum([x*y for (x, y) in zip(cnpj, weightlist(len(cnpj)))]) % 11)

            # if digit is smaller than 2, turns 0
            if r < 2:
                f = 0
            else:
                f = 11 - r

            # append digit to cnpj
            cnpj.append(f)

        # if created number is same as original number, cnpj is valid
        return bool(cnpj == self.cnpj)

    @property
    def single(self):
        """ returns single cnpj number (without '.', '/' and '-') """
        return u''.join([str(x) for x in self.cnpj])

# Based in http://www.python.org.br/wiki/VerificadorDeCpf
class CPF(object):
    """
    This class represents a CPF number
    A CPF number is compounded by XXX.XXX.XXX-VD. The two last digits are
    verification digits.

    More information:
    http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas

    >>> a = CPF(95524361503)
    >>> b = CPF('95524361503')
    >>> c = CPF('955.243.615-03')
    >>> d = CPF([9, 5, 5, 2, 4, 3, 6, 1, 5, 0, 3])
    >>> e = CPF(['9', '5', '5', '2', '4', '3', '6', '1', '5', '0', '3'])
    >>>
    >>> a == b, a == c, a == d, a == e
    (True, True, True, True)

    """

    # cpfs with same number in all digits isn't valid
    invalid_cpfs=map(lambda x: [x for i in range(11)],xrange(1,9))

    error_messages = {
        'invalid': _(u"Invalid CPF number."),
        'max_digits': _(u"CPF requires at most 11 digits or 14 characters."),
        'digits_only': _(u"CPF requires only numbers, allow '.' and '-' for long format."),
    }

    def __init__(self, cpf):

        # transform list or int or long in a string
        if type(cpf) in (int,long):
            cpf = u"%s" % cpf
        if type(cpf) in (list,tuple):
            cpf= u''.join([str(x) for x in cpf])

        try:
            basestring
        except:
            basestring = (str, unicode)

        # only numbers = 11, numbers + '.' and '_' = 14
        if len(cpf) not in (11,14):
            # need to be xxxxxxxxxxx or xxx.xxx.xxx-xx
            raise ValueError(self.error_messages['max_digits'])

        if isinstance(cpf, basestring):
            # remove characters
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")
            # and check if is digit
            if not cpf.isdigit():
                raise ValueError(self.error_messages['digits_only'])

        # turn into a list of integers
        self.cpf = map(int, cpf)

        # validate number and validation digits
        if not self.is_valid:
            raise ValueError(self.error_messages['invalid'])

    def __getitem__(self, index):
        """
        Returns digit at index in CPF

        >>> a = CPF('95524361503')
        >>> a[9] == '0'
        True
        >>> a[10] == '3'
        True
        >>> a[9] == 0
        False
        >>> a[10] == 3
        False

        """
        return str(self.cpf[index])

    def __repr__(self):
        return "CPF('%s')" % ''.join([str(x) for x in self.cpf])

    def __eq__(self, other):
        """
        >>> a = CPF('95524361503')
        >>> b = CPF('955.243.615-03')
        >>> c = CPF('123.456.789-00')
        >>> a == b
        True
        >>> a != c
        True
        >>> b != c
        True
        """
        if isinstance(other, CPF):
            return self.cpf == other.cpf
        return False

    def __unicode__(self):
        """
        Return CPF in long format, with '.' and '-'. For simple format use
        CPF(..).single property/method

        >>> a = CPF('95524361503')
        >>> str(a)
        u'955.243.615-03'
        """

        d = ((3, "."), (7, "."), (11, "-"))
        s = map(str, self.cpf)

        for i, v in d:
            s.insert(i, v)

        r = ''.join(s)

        return r

    def __str__(self):
        return self.__unicode__()

    def __len__(self):
        return len(self.cpf)

    @property
    def is_valid(self):
        """
        Validates CPF number with 9 digits + validation digits.
        This method is used to __init__ to validate number.
        """
        # check if cpf isn't in invalid_cpfs list
        if self.cpf in self.invalid_cpfs: return False

        # get first nine digits to calculate two verification digits
        cpf = self.cpf[:9]
        # while cpf isn't complete (this runs two loops)
        while len(cpf) < 11:

            # run trought numbers multiplying number (v) by weight (len(cpf)+1-i)
            # and then get sum rest of division by 11 as integer
            r = int(sum(map(lambda(i,v):math.floor((len(cpf)+1-i)*v),enumerate(cpf))) % 11)

            # if digit is smaller than 2, turns 0
            if r < 2:
                f = 0
            else:
                f = 11 -r

            # append to cpf list
            cpf.append(f)

        # if created number is same as original number, cpf is valid
        return bool(cpf == self.cpf)

    def __nonzero__(self):
        return self.is_valid

    @property
    def single(self):
        """ returns single cpf number (without '.' and '-') """
        return u''.join([str(x) for x in self.cpf])

def get_digits(randns,d1weight,d2weight):
    """
    return a tuple with cpf or cnpj digits. we use same method to get
    digits based on numbers and weights
    """

    # GET FIRST CHECK DIGIT

    # multiply by weightlist for first digit
    d1ns = [randns[i]*m for i,m in enumerate(d1weight)]

    # get sum
    d1sum = sum(d1ns)

    # get firts digit. if first digit >= 10, transform in 0
    d1 = int(round(d1sum - (math.floor(d1sum/11)*11)))
    if d1 < 2:
        d1 = 0
    else:
        d1 = 11 - d1

    # GET SECOND CHECK DIGIT

    # multipy by weightlist for second digit, but add first digit in list
    d2ns = (lambda: [(randns+[d1])[i]*m for i,m in enumerate(d2weight)])()

    # get sum
    d2sum = sum(d2ns)

    # get second digit. if second digit >= 10, transform in 0
    d2 = int(round(d2sum - (math.floor(d2sum/11)*11)))
    if d2 < 2:
        d2 = 0
    else:
        d2 = 11 - d2

    return d1,d2

def CPFGenerator(amount=1,cpfn=None):
    """ generate valid cpf for tests """

    # randnumbers are created from 0 to 9, and multiplicated by these list for
    # fist digit
    d1weight = range(2,11) # [2,3,...,10]
    d1weight.reverse()

    # for second digit same as for first digit, but with d1
    d2weight = range(2,12) # [2,3,...,11]
    d2weight.reverse()

    # create how many cpfs amount says then add to set cpfs 
    cpfs=set()

    while len(cpfs) < amount:
        # get some rand numbers
        if not cpfn:
            randns = [randint(0,9) for x in range(9)]
        else:
            randns = cpfn

        d1,d2 = get_digits(randns,d1weight,d2weight)

        # transform cpf in a string
        cpf = ("%s"*11) % tuple(randns+[d1,d2])

        # if not exist, add in cpfs
        if not cpf in cpfs:
            cpfs.add(cpf)

    cpfs = list(cpfs)
    if len(cpfs) != 1:
        return cpfs
    else:
        return cpfs[0]

def CNPJGenerator(amount=1,cnpjn=None):
    """ generate valid cnpj for tests """

    d1weight = [5,4,3,2,9,8,7,6,5,4,3,2]
    d2weight = [6] + d1weight

    cnpjs=set()

    while len(cnpjs) < amount:

        if not cnpjn:
            randns = [randint(0,9) for x in range(8)] + [0,0,0,randint(0,9)]
        else:
            randns = cnpjn

        d1,d2 = get_digits(randns,d1weight,d2weight)

        # transform cnpj in a string
        cnpj = ("%s"*14) % tuple(randns+[d1,d2])

        # if not exist, add in cnpjs
        if not cnpj in cnpjs:
            cnpjs.add(cnpj)

    cnpjs = list(cnpjs)
    if len(cnpjs) != 1:
        return cnpjs
    else:
        return cnpjs[0]



