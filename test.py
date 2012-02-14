#!/bin/env python
# -*- coding: utf-8 -*-

import unittest
from svalidate import validate, OrNone, Any, Each, NoOne, Equal, RegexpMatch, RegexpSearch, DateTime, Length

class Test(unittest.TestCase):
    def test_something(self, ):
        """
        """
        self.assertEqual(None, validate({}, {}))
        self.assertEqual(None, validate({'name' : '',
                                         'descr' : OrNone(''),
                                         'sharing' : True,
                                         'ruleset' : Any(Equal('despot'),
                                                         Equal('vote')),
                                         'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                                        {'name' : 'blah blah',
                                         'sharing' : False,
                                         'ruleset' : 'despot',
                                         'user_name' : 'vasya'}))
        
        self.assertNotEqual(None, validate({'name' : '',
                                            'descr' : OrNone(''),
                                            'sharing' : True,
                                            'ruleset' : Any(Equal('despot'),
                                                            Equal('vote')),
                                            'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                                           {'name' : 'blah blah',
                                            'sharing' : False,
                                            'ruleset' : 'despot',
                                            'user_name' : 'va<sya'}))

        self.assertNotEqual(None, validate({'name' : '',
                                            'descr' : OrNone(''),
                                            'sharing' : True,
                                            'ruleset' : Any(Equal('despot'),
                                                            Equal('vote')),
                                            'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                                           {'name' : 'blah blah',
                                            'sharing' : False,
                                            'ruleset' : 'despsot',
                                            'user_name' : 'vasya'}))

        self.assertEqual(None, validate({'name' : '',
                                         'descr' : OrNone(''),
                                         'sharing' : True,
                                         'ruleset' : Any(Equal('despot'),
                                                         Equal('vote')),
                                         'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                                        {'name' : 'blah blah',
                                         'sharing' : False,
                                         'ruleset' : 'vote',
                                         'user_name' : 'vasya'}))
        
        self.assertNotEqual(None, validate({'name' : '',
                                            'descr' : OrNone(''),
                                            'sharing' : True,
                                            'ruleset' : Any(Equal('despot'),
                                                            Equal('vote')),
                                            'user_name' : NoOne(RegexpSearch(r'[<>]'))},
                                           {'name' : 'blah blah',
                                            'descr' : 234234,
                                            'sharing' : False,
                                            'ruleset' : 'despot',
                                            'user_name' : 'vasya'}))
        goodstr = RegexpMatch(r'^[^<>]*$')
        self.assertNotEqual(None, validate({'name' : goodstr,
                                            'descr' : OrNone(goodstr),
                                            'sharing' : True,
                                            'ruleset' : Any(Equal('despot'),
                                                            Equal('vote')),
                                            'user_name' : goodstr},
                                           {'name' : 'bl<ah blah',
                                            'sharing' : False,
                                            'ruleset' : 'despot',
                                            'user_name' : 'vasya'}))

        self.assertNotEqual(None, validate({'name' : goodstr,
                                            'descr' : OrNone(goodstr),
                                            'sharing' : True,
                                            'ruleset' : Any(Equal('despot'),
                                                            Equal('vote')),
                                            'user_name' : goodstr},
                                           {'name' : 'blah blah',
                                            'sharing' : False,
                                            'descr' : 'asdf<script>',
                                            'ruleset' : 'despot',
                                            'user_name' : 'vasya'}))

        self.assertEqual(None, validate({'uuid' : '',
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

        self.assertNotEqual(None, validate({'uuid' : '',
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
                                                        {'value' : 'eijfijf'}]}))

        self.assertNotEqual(None, validate({'uuid' : '',
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
                                            'descr' : 'isjd > ',
                                            'tp' : 'ijsijs',
                                            'enum' : True,
                                            'values' : [{'value' : 'jsijs',
                                                         'caption' : 'isjijs'},
                                                        {'value' : 'eijfijf'}]}))

        self.assertNotEqual(None, validate({'uuid' : '',
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
                                                        {'value' : 'eijfijf'}]}))

        self.assertNotEqual(None, validate({'uuid' : '',
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
                                                        {'value' : 'eijfijf'}]}))

        self.assertEqual(None, validate(DateTime(), {'year' : 1999,
                                                     'month' : 10,
                                                     'day' : 20,
                                                     'hour' : 20,
                                                     'minute' : 22,
                                                     'second' : 22}))

        self.assertNotEqual(None, validate(DateTime(), {'year' : 1999,
                                                        'month' : 13,
                                                        'day' : 20,
                                                        'hour' : 20,
                                                        'minute' : 22,
                                                        'second' : 22}))
        self.assertNotEqual(None, validate(DateTime(), {'year' : 2000.23,
                                                        'month' : 10,
                                                        'day' : 20,
                                                        'hour' : 20,
                                                        'minute' : 22,
                                                        'second' : 22}))
        self.assertNotEqual(None, validate(DateTime(), {'year' : 1999,
                                                        'month' : 10,
                                                        'day' : 20,
                                                        'hour' : 20,
                                                        'minute' : 44,
                                                        'second' : '22'}))
        self.assertNotEqual(None, validate(DateTime(), {'year' : 1999,
                                                        'month' : 10,
                                                        'day' : 20,
                                                        'hour' : 20,
                                                        'minute' : 22,
                                                        'second' : 60}))

        self.assertEqual(None, validate(Length(low=2), "sdf"))
        self.assertEqual(None, validate(Length(high=10), "asdfa"))
        self.assertEqual(None, validate(Length(4, 7), "12345"))
        
        self.assertNotEqual(None, validate(Length(low=2), "f"))
        self.assertNotEqual(None, validate(Length(high=10), "asdfssssssssssssa"))
        self.assertNotEqual(None, validate(Length(4, 7), "345"))
        self.assertNotEqual(None, validate(Length(2, 3), 33))
        


if __name__ == "__main__":
    unittest.main()
