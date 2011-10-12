# coding: utf-8

def to_unicode(s):
    """
    Receive string s and try to return a utf-8 string.
    """
    try:
        return unicode(s.decode('cp1252'))
    except (UnicodeDecodeError,TypeError):
        try:
            return unicode(s.decode('ascii'))
        except (UnicodeDecodeError,TypeError):
            return unicode(s)
