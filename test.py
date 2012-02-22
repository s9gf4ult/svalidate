#!/bin/env python
# -*- coding: utf-8 -*-

import unittest
from svalidate import Validate, OrNone, Any, Each, NoOne, Equal, RegexpMatch, RegexpSearch, DateTime, DateTimeString, Length, \
    JsonString, Able, NO_ONE_VALIDATION_FAILED, EQUAL_VALIDATION_FAILED, VALUE_IS_NOT_A_STRING, ANY_VALIDATION_FAILED,\
    REGEXP_MATCH_FAILED, VALUE_IS_NOT_A_BOOLEAN, DATETIME_VALIDATION_FAILED, VALUE_IS_NOT_AN_INT, LENGTH_VALIDATION_FAILED, \
    EACH_VALIDATION_FAILED, JSON_VALIDATION_FAILED, CAN_NOT_PROCESS_VALUE
import json

class Test(unittest.TestCase):
    def test_something(self, ):
        """
        """
        v = Validate()
        self.assertEqual(None, v.validate({}, {}))
        self.assertEqual(None, v.validate({'name' : '',
                                           'descr' : OrNone(''),
                                           'sharing' : True,
                                           'ruleset' : Any(Equal('despot'),
                                                           Equal('vote')),
                                           'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                                          {'name' : 'blah blah',
                                           'sharing' : False,
                                           'ruleset' : 'despot',
                                           'user_name' : 'vasya'}))

        r =  v.validate({'name' : '',
                         'descr' : OrNone(''),
                         'sharing' : True,
                         'ruleset' : Any(Equal('despot'),
                                         Equal('vote')),
                         'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                        {'name' : 'blah blah',
                         'sharing' : False,
                         'ruleset' : 'despot',
                         'user_name' : 'va<sya'})
        self.assertEqual(1, len(r))
        self.assertEqual(r[0]['type'], 'dictionary')
        self.assertEqual(r[0]['code'], 'user_name')
        self.assertEqual(r[0]['error'][0]['type'], 'value')
        self.assertEqual(r[0]['error'][0]['code'], NO_ONE_VALIDATION_FAILED)
        self.assertEqual(None, v.validate([{'type' : Equal('dictionary'),
                                            'code' : Equal('user_name'),
                                            'error' : [{'type' : Equal('value'),
                                                        'code' : Equal(NO_ONE_VALIDATION_FAILED),
                                                        'caption' : ''}]}],
                                          r)) # recursive validation !!

        r = v.validate({'name' : '',
                        'descr' : OrNone(''),
                        'sharing' : True,
                        'ruleset' : Any(Equal('despot'),
                                        Equal('vote')),
                        'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                       {'name' : 'blah blah',
                        'sharing' : False,
                        'ruleset' : 'despsot',
                        'user_name' : 'vasya'})

        self.assertEqual(None, v.validate([{'type' : Equal('dictionary'),
                                            'code' : Equal('ruleset'),
                                            'error' : [{'type' : Equal('value'),
                                                        'code' : Equal(ANY_VALIDATION_FAILED)}]}],
                                          r))

        self.assertEqual(None, v.validate({'name' : '',
                                           'descr' : OrNone(''),
                                           'sharing' : True,
                                           'ruleset' : Any(Equal('despot'),
                                                           Equal('vote')),
                                           'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                                          {'name' : 'blah blah',
                                           'sharing' : False,
                                           'ruleset' : 'vote',
                                           'user_name' : 'vasya'}))

        r = v.validate({'name' : '',
                        'descr' : OrNone(''),
                        'sharing' : True,
                        'ruleset' : Any(Equal('despot'),
                                        Equal('vote')),
                        'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                       {'name' : 'blah blah',
                        'descr' : 234234,
                        'sharing' : False,
                        'ruleset' : 'despot',
                        'user_name' : 'vasya'})

        self.assertEqual(None, v.validate([{'type' : Equal('dictionary'),
                                            'code' : Equal('descr'),
                                            'error' : [{'type' : Equal('value'),
                                                        'code' : Equal(VALUE_IS_NOT_A_STRING)}]}],
                                          r))




        goodstr = RegexpMatch(r'^[^<>]*$')
        r = v.validate({'name' : goodstr,
                        'descr' : OrNone(goodstr),
                        'sharing' : True,
                        'ruleset' : Any(Equal('despot'),
                                        Equal('vote')),
                        'user_name' : goodstr},
                       {'name' : 'bl<ah blah',
                        'sharing' : False,
                        'ruleset' : 'despot',
                        'user_name' : 'vasya'})

        self.assertEqual(None, v.validate([{'type' : Equal('dictionary'),
                                            'code' : Equal('name'),
                                            'error' : [{'type' : Equal('value'),
                                                        'code' : Equal(REGEXP_MATCH_FAILED)}]}],
                                          r))


        self.assertEqual(None, v.validate({'uuid' : '',
                                           'name' : goodstr,
                                           'descr' : OrNone(goodstr),
                                           'tp' : '',
                                           'enum' : True,
                                           'default' : OrNone(goodstr),
                                           'values' : OrNone([{'value' : goodstr,
                                                               'caption' : OrNone(goodstr),
                                                               }]),
                                           },

                                          {'uuid' : 'sdf323rsd9fusdf',
                                           'name' : 'you',
                                           'tp' : 'ijsijs',
                                           'enum' : True,
                                           'values' : [{'value' : 'jsijs',
                                                        'caption' : 'isjijs'},
                                                       {'value' : 'eijfijf'}]}))

        r = v.validate({'uuid' : '',
                        'name' : goodstr,
                        'descr' : OrNone(goodstr),
                        'tp' : '',
                        'enum' : True,
                        'default' : OrNone(goodstr),
                        'values' : OrNone([{'value' : goodstr,
                                            'caption' : OrNone(goodstr),
                                            }]),
                        },
                       {'uuid' : 'sdf323rsd9fusdf',
                        'name' : '<you',
                        'tp' : 'ijsijs',
                        'enum' : True,
                        'values' : [{'value' : 'jsijs',
                                     'caption' : 'isjijs'},
                                    {'value' : 'eijfijf'}]})

        self.assertEqual(None, v.validate([{'type' : Equal('dictionary'),
                                            'code' : Equal('name'),
                                            'error' : [{'type' : Equal('value'),
                                                        'code' : Equal(REGEXP_MATCH_FAILED)}]}],
                                          r))



        r = v.validate({'uuid' : '',
                        'name' : goodstr,
                        'descr' : OrNone(goodstr),
                        'tp' : '',
                        'enum' : True,
                        'default' : OrNone(goodstr),
                        'values' : OrNone([{'value' : goodstr,
                                            'caption' : OrNone(goodstr),
                                            }]),
                        },
                       {'uuid' : 'sdf323rsd9fusdf',
                        'name' : 'you',
                        'tp' : 'ijsijs',
                        'enum' : 'True',
                        'values' : [{'value' : 'jsijs',
                                     'caption' : 'isjijs'},
                                    {'value' : 'eijfijf'}]})

        self.assertEqual(None, v.validate([{'type' : Equal('dictionary'),
                                            'code' : Equal('enum'),
                                            'error' : [{'type' : Equal('value'),
                                                        'code' : Equal(VALUE_IS_NOT_A_BOOLEAN)}]}],
                                          r))

        r = v.validate({'uuid' : '',
                        'name' : goodstr,
                        'descr' : OrNone(goodstr),
                        'tp' : '',
                        'enum' : True,
                        'default' : OrNone(goodstr),
                        'values' : OrNone([{'value' : goodstr,
                                            'caption' : OrNone(goodstr),
                                            }]),
                        },

                       {'uuid' : 'sdf323rsd9fusdf',
                        'name' : 'you',
                        'tp' : 'ijsijs',
                        'enum' : True,
                        'values' : [{'value' : 'jsijs',
                                     'caption' : 'is>jijs'},
                                    {'value' : 'eijfijf'}]})

        self.assertEqual(None, v.validate([{'type' : Equal('dictionary'),
                                            'code' : Equal('values'),
                                            'error' : [{'type' : Equal('list'),
                                                        'code' : Equal(0),
                                                        'error' : [{'type' : Equal('dictionary'),
                                                                    'code' : Equal('caption'),
                                                                    'error' : [{'type' : Equal('value'),
                                                                                'code' : Equal(REGEXP_MATCH_FAILED)}]}]}]}], # Recursive validation forewer !
                                          r))

        self.assertEqual(None, v.validate(DateTime(), {'year' : 1999,
                                                       'month' : 10,
                                                       'day' : 20,
                                                       'hour' : 20,
                                                       'minute' : 22,
                                                       'second' : 22}))

        r = v.validate(DateTime(), {'year' : 1999,
                                    'month' : 13,
                                    'day' : 20,
                                    'hour' : 20,
                                    'minute' : 22,
                                    'second' : 22})

        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(DATETIME_VALIDATION_FAILED),
                                            'caption' : ''}],
                                          r))

        r = v.validate(DateTime(), {'year' : 2000.23,
                                    'month' : 10,
                                    'day' : 20,
                                    'hour' : 20,
                                    'minute' : 22,
                                    'second' : 22})
        self.assertEqual(None, v.validate([{'type' : Equal('dictionary'),
                                            'code' : Equal('year'),
                                            'error' : [{'type' : Equal('value'),
                                                        'code' : Equal(VALUE_IS_NOT_AN_INT)}]}],
                                          r))



        self.assertEqual(None, v.validate(Length(low=2), "sdf"))
        self.assertEqual(None, v.validate(Length(high=10), "asdfa"))
        self.assertEqual(None, v.validate(Length(4, 7), "12345"))

        r = v.validate(Length(low=2), "f")
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                           'code' : Equal(LENGTH_VALIDATION_FAILED)}],
                                          r))

        r = v.validate(Length(high=10), "asdfssssssssssssa")
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(LENGTH_VALIDATION_FAILED)}],
                                          r))

        r = v.validate(Length(4, 7), "345")
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(LENGTH_VALIDATION_FAILED)}],
                                          r))
        r = v.validate(Length(2, 3), 33)
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(LENGTH_VALIDATION_FAILED)}],
                                          r))

        self.assertEqual(None, v.validate(Each(Length(0, 10), ''), 'sdfa'))
        self.assertEqual(None, v.validate(Each(Length(high = 4), ['']), ['sd', 'ss']))
        r = v.validate(Each(Length(1, 5), []), [])
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(EACH_VALIDATION_FAILED),
                                            'error' : [{'type' : Equal('value'),
                                                        'code' : Equal(LENGTH_VALIDATION_FAILED)}]}],
                                          r))
        r = v.validate(Each(Length(high=2), ['']), [0, 'asdf', 'asdf'])

        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(EACH_VALIDATION_FAILED),
                                            'error' : [Any({'type' : Equal('value'),
                                                            'code' : Equal(LENGTH_VALIDATION_FAILED)},
                                                           {'type' : Equal('list'),
                                                            'code' : Equal(0),
                                                            'error' : [{'type' : Equal('value'),
                                                                        'code' : Equal(VALUE_IS_NOT_A_STRING)}]})]}],
                                          r))

        self.assertEqual(None, v.validate(DateTimeString(), '2010-10-20T20:20:20'))
        self.assertEqual(None, v.validate(DateTimeString(), '2010-10-20 20:20:20'))
        self.assertEqual(None, v.validate(DateTimeString(), '1984-01-20T20:20:20'))
        r = v.validate(DateTimeString(), 'ajisdjfasd')
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(DATETIME_VALIDATION_FAILED)}],
                                          r))
        r = v.validate(DateTimeString(), '0000-10-20T20:20:20')
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(DATETIME_VALIDATION_FAILED)}],
                                          r))
        r = v.validate(DateTimeString(), '1234-10-44T20:20:20')
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(DATETIME_VALIDATION_FAILED)}],
                                          r))
        r = v.validate(DateTimeString(), '2000-10-20T20:20:60')
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(DATETIME_VALIDATION_FAILED)}],
                                          r))
        self.assertEqual(None, v.validate(DateTimeString(), '2010-10-20'))

        enc = json.JSONEncoder()
        
        self.assertEqual(None, v.validate(JsonString({'uuid' : '',
                                                      'name' : goodstr,
                                                      'descr' : OrNone(goodstr),
                                                      'tp' : '',
                                                      'enum' : True,
                                                      'default' : OrNone(goodstr),
                                                      'values' : OrNone([{'value' : goodstr,
                                                                          'caption' : OrNone(goodstr),
                                                                          }]),
                                                      }),

                                          enc.encode({'uuid' : 'sdf323rsd9fusdf',
                                                      'name' : 'you',
                                                      'tp' : 'ijsijs',
                                                      'enum' : True,
                                                      'values' : [{'value' : 'jsijs',
                                                                   'caption' : 'isjijs'},
                                                                  {'value' : 'eijfijf'}]})))

        r = v.validate(JsonString({'name' : goodstr}),
                       'asdfasdf')
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(JSON_VALIDATION_FAILED)}],
                                          r))

        self.assertEqual(None, v.validate(Able(int), "   424   "))
        self.assertEqual(None, v.validate(Able(float), '   24.'))
        r = v.validate(Able(int), '    2444.  ')
        self.assertEqual(None, v.validate([{'type' : Equal('value'),
                                            'code' : Equal(CAN_NOT_PROCESS_VALUE)}],
                                          r))
        self.assertRaises(ValueError, Able, 'not callable argument')


if __name__ == "__main__":
    unittest.main()
