#!/bin/env python
# -*- coding: utf-8 -*-

import unittest
from svalidate import validate, OrNone, Any, Each, NoOne, Equal, RegexpMatch, RegexpSearch

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





if __name__ == "__main__":
    unittest.main()
