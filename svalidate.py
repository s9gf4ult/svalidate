#! /bin/env python
# -*- coding: utf-8 -*-

import re
import datetime


def validate(template, data):
    """Validate data by template
    
    Arguments:
    - `template`:
    - `data`:
    """
    return _validate(u"Root element {0}", template, data)
    
def _validate(formater, template, data):
    """Validate data by template
    Arguments:
    - `formater`: string formating by one argument
    - `template`:structure 
    - `data`:
    Returns: string with validation error description or None if no one
    """
    t = type(template)
    if t in _dispatch:
        res = _dispatch[t](template, data)
        if res != None:
            return formater.format(res)
        return None
    elif isinstance(template, Validator):
        res = template(data)
        if res != None:
            return formater.format(res)
        return None
    else:
        raise ValueError(u"Template is not valid, type {0} not in dispatch".format(t))

def dictDispatch(template, data):
    """Dispatch over each value in data by each key in template
    Arguments:
    - `template`:
    - `data`:
    Return: string with error description or None if no errors in validation
    """
    if isinstance(data, dict):
        for tkey in template.keys():
            r = _validate(u'-> key element "{0}" {{0}}'.format(tkey), template[tkey], data.get(tkey))
            if r != None:
                return r
        return None
    return u': element is not a dictionary'

def listDispatch(template, data):
    """Dispatch over each element in data by first argument in template
    Arguments:
    - `template`:
    - `data`:
    """
    if isinstance(data, list):
        if len(template) == 0:
            return None
        vdr = template[0]
        for nmb, elt in zip(xrange(len(data)), data):
            r = _validate(u'-> list element {0} {{0}}'.format(nmb), vdr, elt)
            if r != None:
                return r
        return None
    else:
        return u': is not a list'

def setDispatch(template, data):
    """Dispatch over each element in data by first argument in template
    Arguments:
    - `template`:
    - `data`:
    """
    if isinstance(data, set):
        if len(template) == 0:
            return None
        vdr = template.__iter__().next()   # thats because we deal with python
        for nmb, elt in zip(xrange(len(data)), data):
            r = _validate(u'-> set element {0} {{0}}'.format(nmb), vdr, elt)
            if r != None:
                return r
        return None
    else:
        return u': is not a set'

            
def intDispatch(template, data):
    """Check if data is int
    Arguments:
    - `template`:
    - `data`:
    """
    if isinstance(data, int):
        return None
    return u': "{0}" is not an int'.format(data)

def strDispatch(template, data):
    """Check if data is string
    Arguments:
    - `template`:
    - `data`:
    """
    if isinstance(data, basestring):
        return None
    return u': "{0}" is not a string'.format(data)

def boolDispatch(template, data):
    """
    Arguments:
    - `template`:
    - `data`:
    """
    if isinstance(data, bool):
        return None
    return u': "{0}" is not a boolean'.format(data)

def floatDispatch(template, data):
    """
    Arguments:
    - `template`:
    - `data`:
    """
    if isinstance(data, float):
        return None
    return u': "{0}" is not a float'.format(data)

class Validator(object):
    """common validator object
    """
    def __call__(self, data):
        """
        """
        raise NotImplementedError(u'You must implement call method of validator')
    

class OrNone(Validator):
    """Validates if 
    """
    
    def __init__(self, validator):
        """
        Arguments:
        - `validator`: any validator which will be passed if data is not None
        """
        self._validator = validator
        
    def __call__(self, data):
        """
        Arguments:
        - `data`:
        """
        if data == None:
            return None
        else:
            return _validate('{0}', self._validator, data)

class Any(Validator):
    """
    """
    
    def __init__(self, *validators):
        """
        Arguments:
        - `*validators`: validators any of which may pass validation
        """
        if len(validators) == 0:
            raise ValueError('Wrong template: `Any` validator must have at least one argument')
        self._validators = validators

    def __call__(self, data):
        """
        Arguments:
        - `data`:
        """
        r = None
        for v in self._validators:
            r = _validate(u': Any validation is not passed {0}', v, data)
            if r == None:
                return None
        return r


class Each(Validator):
    """
    """
    
    def __init__(self, *validators):
        """
        
        Arguments:
        - `*validators`:
        """
        if len(validators) == 0:
            raise ValueError(u'Wrong template: Each validator must have at least one argument')
        self._validators = validators

    def __call__(self, data):
        """
        Arguments:
        - `data`:
        """
        for v in self._validators:
            r = _validate(': Each validator is not passed {0}', v, data)
            if r != None:
                return r
        return None

class NoOne(Validator):
    """
    """
    
    def __init__(self, *validators):
        """
        Arguments:
        - `*validators`:
        """
        if len(validators) == 0:
            raise ValueError(u'Wrong template: NoOne validator must have at least one argument')
        self._validators = validators

    def __call__(self, data):
        """
        Arguments:
        - `data`:
        """
        for v in self._validators:
            r = _validate(u'{0}', v, data)
            if r == None:
                return u': NoOne failed, validator "{0}" passed on "{1}"'.format(type(v), data)
        return None

class Equal(Validator):
    """
    """
    
    def __init__(self, value):
        """
        Arguments:
        - `value`:
        """
        self._value = value

    def __call__(self, data):
        """
        Arguments:
        - `data`:
        """
        if data != self._value:
            return u': "{0}" is not equal to "{1}"'.format(data, self._value)
        else:
            return None

class RegexpSearch(Validator):
    """
    """
    
    def __init__(self, regexp):
        """
        
        Arguments:
        - `regexp`:
        """
        self._re = re.compile(regexp)
        self._patern = regexp

    def __call__(self, data):
        """
        Arguments:
        - `data`:
        """
        r = _validate(': RegexpSearch validator {0}', '', data)
        if r != None:
            return r
        if self._re.search(data) != None:
            return None
        else:
            return ': RegexpSearch did not found pattern "{0}" in "{1}"'.format(self._patern, data)

class RegexpMatch(Validator):
    """
    """
    
    def __init__(self, regexp):
        """
        
        Arguments:
        - `regexp`:
        """
        self._re = re.compile(regexp)
        self._patern = regexp

    def __call__(self, data):
        """
        Arguments:
        - `data`:
        """
        r = _validate(': RegexpMatch validator {0}', '', data)
        if r != None:
            return r
        if self._re.match(data) != None:
            return None
        else:
            return ': RegexpMatch "{0}" does not match pattern "{1}"'.format(data, self._patern)

class DateTime(Validator):
    """
    """
    def __call__(self, data):
        """
        Arguments:
        - `data`:
        """
        r = _validate(u': DateTime {0}', {'year' : 0,
                                          'month' : 0,
                                          'day' : 0,
                                          'hour' : 0,
                                          'minute' : 0,
                                          'second' : 0}, data)
        if r != None:
            return r
        try:
            datetime.datetime(*[data[a] for a in ['year', 'month', 'day', 'hour', 'minute', 'second']])
        except Exception as e:
            return u': can not construct datetime because {0}'.format(str(e))
        else:
            return None

class Length(Validator):
    """
    """
    
    def __init__(self, low=0, high=None):
        """
        Arguments:
        
        - `low`:
        - `high`:
        """
        self._low = low
        self._high = high

    def __call__(self, data):
        """
        Arguments:
        
        - `data`:
        """
        l = None
        try:
            l = len(data)
        except Exception as e:
            return u': {0}'.format(str(e))
        if self._high != None:
            if not (self._low <= l <= self._high):
                return u': length must be between {0} and {1}, not {2}'.format(self._low, self._high, l)
        else:
            if not (self._low <= l):
                return u': length must be grather than {0}, not {1}'.format(self._low, l)
        return None
    
        
        
            
_dispatch = {dict : dictDispatch,
             list : listDispatch,
             set : setDispatch,
             int : intDispatch,
             str : strDispatch,
             bool : boolDispatch,
             float : floatDispatch,
             unicode : strDispatch,
             }
