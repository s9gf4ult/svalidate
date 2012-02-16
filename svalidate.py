#! /bin/env python
# -*- coding: utf-8 -*-

import re
import datetime

VALUE_IS_NOT_A_DICTIONARY=0
VALUE_IS_NOT_A_LIST=1
VALUE_IS_NOT_A_SET=2
VALUE_IS_NOT_AN_INT=3
VALUE_IS_NOT_A_FLOAT=4
VALUE_IS_NOT_A_BOOLEAN=5
VALUE_IS_NOT_A_STRING=6
ANY_VALIDATION_FAILED=7
NO_ONE_VALIDATION_FAILED=8
EACH_VALIDATION_FAILED=9
REGEXP_MATCH_FAILED=10
REGEXP_SEARCH_FAILED=11
EQUAL_VALIDATION_FAILED=12
DATETIME_VALIDATION_FAILED=13
LENGTH_VALIDATION_FAILED=14


class Validate(object):

    def __init__(self, ):
        """
        """
        self._dispatch = {dict : self.dictDispatch,
                          list : self.listDispatch,
                          set : self.setDispatch,
                          int : self.intDispatch,
                          str : self.strDispatch,
                          bool : self.boolDispatch,
                          float : self.floatDispatch,
                          unicode : self.strDispatch,
                          }


    def validate(self, template, data):
        """Validate data by template
        
        Arguments:
        
        - `template`: any acceptable validator
        - `data`:

        Return None if data validated. Otherwise return list of dictionaries with keys:
        
        - `type`: type of error, one of posible:
           - `'value'`: value is not of valid type
           - `'dictionary'`: error of value in dictionary
           - `'list'`: error of value in list
           - `'set'`: error of value in set
        - `code`: if `type` is 'dictionary' then `code` is key of dictionary.
          If `type` is 'list' or 'set' then code is int with index of list where error was occured.
          If `type` is 'value' then `code` is error code declared above
        - `error`: if `type` is 'dictionary' or 'list' or 'set' then `error` is dictionary with embedded error
        - `caption`: human readable description if `type` == 'value'
        """
        self.errors = []
        self._validate(self.errors, template, data)
        if len(self.errors) == 0:
            return None
        else:
            return self.errors
    
    
    def _validate(self, appender, template, data):
        t = type(template)
        if t in self._dispatch:
            self._dispatch[t](appender, template, data)
        elif isinstance(template, Validator):
            template(self, appender, data)
        else:
            raise ValueError(u"Template is not valid, type {0} not in dispatch".format(t))

    def dictDispatch(self, appender, template, data):
        if isinstance(data, dict):
            for tkey in template.keys():
                erl = []
                self._validate(erl, template[tkey], data.get(tkey))
                if len(erl) > 0:
                    appender.append({'type' : 'dictionary',
                                     'code' : tkey,
                                     'error' : erl})
        else:
            appender.append({'type' : 'value',
                             'code' : VALUE_IS_NOT_A_DICTIONARY,
                             'caption' : '{0} is not a dictionary'.format(data)})

    def listDispatch(self, appender, template, data):
        if isinstance(data, list):
            if len(template) == 0:
                return
            vdr = template[0]

            for nmb, elt in zip(xrange(len(data)), data):
                erl = []
                self._validate(erl, vdr, elt)
                if len(erl) > 0:
                    appender.append({'type' : 'list',
                                     'code' : nmb,
                                     'error' : erl})
        else:
            appender.append({'type' : 'value',
                             'code' : VALUE_IS_NOT_A_LIST,
                             'caption' : '{0} is not a list'.format(data)})

    def setDispatch(self, appender, template, data):
        if isinstance(data, set):
            if len(template) == 0:
                return
            vdr = template.__iter__().next()
            for nmb, elt in zip(xrange(len(data)), data):
                erl = []
                self._validate(erl, vdr, elt)
                if len(erl) > 0:
                    appender.append({'type' : 'set',
                                     'code' : nmb,
                                     'error' : erl})
        else:
            appender.append({'type' : 'value',
                             'code' : VALUE_IS_NOT_A_SET,
                             'caption' : '{0} is not a set'.format(data)})


    def intDispatch(self, appender, template, data):
        if isinstance(data, int):
            return
        appender.append({'type' : 'value',
                         'code' : VALUE_IS_NOT_AN_INT,
                         'caption' : '{0} is not an integer'.format(data)})

    def strDispatch(self, appender, template, data):
        if isinstance(data, basestring):
            return
        appender.append({'type' : 'value',
                         'code' : VALUE_IS_NOT_A_STRING,
                         'caption' : '{0} is not a string'.format(data)})

    def boolDispatch(self, appender, template, data):
        if isinstance(data, bool):
            return
        appender.append({'type' : 'value',
                         'code' : VALUE_IS_NOT_A_BOOLEAN,
                         'caption' : '{0} is not a boolean'.format(data)})

    def floatDispatch(self, template, data):
        if isinstance(data, float):
            return
        appender.append({'type' : 'value',
                         'code' : VALUE_IS_NOT_A_FLOAT,
                         'caption' : '{0} is not a float'.format(data)})

    

class Validator(object):
    """common validator object
    """
    def __call__(self, appender, data):
        """
        """
        raise NotImplementedError(u'You must implement call method of validator')
    

class OrNone(Validator):
    """passes embedded validator if value is not None, else do nothing
    """
    
    def __init__(self, validator):
        self._validator = validator
        
    def __call__(self, vdr, appender, data):
        if data == None:
            return
        else:
            vdr._validate(appender, self._validator, data)

class Any(Validator):
    """validates if any of given validators are passed
    """
    
    def __init__(self, *validators):
        if len(validators) == 0:
            raise ValueError('Wrong template: `Any` validator must have at least one argument')
        self._validators = validators

    def __call__(self, vdr, appender, data):
        erls = []
        for v in self._validators:
            erl = []
            vdr._validate(erl, v, data)
            if len(erl) == 0:
                return
            erls.append(erl[0])
        appender.append({'type' : 'value',
                         'code' : ANY_VALIDATION_FAILED,
                         'error' : erls})


class Each(Validator):
    """validates if each of given validators are passed
    """
    
    def __init__(self, *validators):
        if len(validators) == 0:
            raise ValueError(u'Wrong template: Each validator must have at least one argument')
        self._validators = validators

    def __call__(self, vdr, appender, data):
        erl = []
        for v in self._validators:
            vdr._validate(erl, v, data)
        if len(erl) == 0:
            return
        appender.append({'type' : 'value',
                         'code' : EACH_VALIDATION_FAILED,
                         'error' : erl})

class NoOne(Validator):
    """validates if no one of given validators is passed
    """
    
    def __init__(self, *validators):
        if len(validators) == 0:
            raise ValueError(u'Wrong template: NoOne validator must have at least one argument')
        self._validators = validators

    def __call__(self, vdr, appender, data):
        erl = []
        for v in self._validators:
            vdr._validate(erl, v, data)
            
        if len(erl) == len(self._validators):
            return
        appender.append({'type' : 'value',
                         'code' : NO_ONE_VALIDATION_FAILED,
                         'caption' : 'One of embedded validators are passed'})

class Equal(Validator):
    """validates if value is equal to given value
    """
    
    def __init__(self, value):
        self._value = value

    def __call__(self, vdr, appender, data):
        if data != self._value:
            appender.append({'type' : 'value',
                             'code' : EQUAL_VALIDATION_FAILED,
                             'caption' : '{0} is not equal to {1}'.format(data, self._value)})

class RegexpSearch(Validator):
    """
    """
    
    def __init__(self, regexp):
        self._re = re.compile(regexp)
        self._patern = regexp

    def __call__(self, vdr, appender, data):
        erl = []
        vdr._validate(erl, '', data)
        if len(erl)>0:
            appender.append(erl[0])
            return
        
        if self._re.search(data) != None:
            return
        else:
            appender.append({'type' : 'value',
                             'code' : REGEXP_SEARCH_FAILED,
                             'caption' : 'RegexpSearch did not found pattern "{0}" in "{1}"'.format(self._patern, data)})
        

class RegexpMatch(Validator):
    """
    """
    
    def __init__(self, regexp):
        self._re = re.compile(regexp)
        self._patern = regexp

    def __call__(self, vdr, appender, data):
        erl=[]
        vdr._validate(erl, '', data)
        if len(erl) > 0:
            appender.append(erl[0])
            return
        if self._re.match(data) != None:
            return
        else:
            appender.append({'type' : 'value',
                             'code' : REGEXP_MATCH_FAILED,
                             'caption' : 'RegexpMatch "{0}" does not match pattern "{1}"'.format(data, self._patern)})

class DateTime(Validator):
    """
    """
    def __call__(self, vdr, appender, data):
        erl = []
        vdr._validate(erl, {'year' : 0,
                            'month' : 0,
                            'day' : 0,
                            'hour' : 0,
                            'minute' : 0,
                            'second' : 0}, data)
        if len(erl) > 0:
            appender += erl
            return
        try:
            datetime.datetime(*[data[a] for a in ['year', 'month', 'day', 'hour', 'minute', 'second']])
        except Exception as e:
            appender.append({'type' : 'value',
                             'code' : DATETIME_VALIDATION_FAILED,
                             'caption' : 'can not construct datetime because {0}'.format(str(e))})

class DateTimeString(Validator):
    def __call__(self, vdr, appender, data):
        erl = []
        vdr._validate(erl, '', data)
        if len(erl) > 0:
            appender += erl
            return
        for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
            try:
                datetime.datetime.strptime(data, fmt)
            except ValueError:
                pass
            else:
                return
        appender.append({'type' : 'value',
                         'code' : DATETIME_VALIDATION_FAILED,
                         'caption' : u'value {0} does not match datetime format'.format(data)})

class Length(Validator):
    
    def __init__(self, low=0, high=None):
        self._low = low
        self._high = high

    def __call__(self, vdr, appender, data):
        l = None
        try:
            l = len(data)
        except Exception as e:
            appender.append({'type' : 'value',
                             'code' : LENGTH_VALIDATION_FAILED,
                             'caption' : str(e)})
            return
        if self._high != None:
            if not (self._low <= l <= self._high):
                appender.append({'type' : 'value',
                                 'code' : LENGTH_VALIDATION_FAILED,
                                 'caption' : 'length must be between {0} and {1}, not {2}'.format(self._low, self._high, l)})
        else:
            if not (self._low <= l):
                appender.append({'type' : 'value',
                                 'code' : LENGTH_VALIDATION_FAILED,
                                 'caption' : 'length must be grather than {0}, not {1}'.format(self._low, l)})
        return
    
        
        
            
