# coding: utf-8
from django.utils.translation import ugettext_lazy as _

class UnknowSource(Exception):
    msg = _(u"The source file can't be opened")
    def __init__(self,err=None):
        if err:
            self.msg = _(u"%(msg)s, the error was: %(err)s") % {'msg':self.msg,'err':err}

