#!/usr/bin/env python

####
#### By Elim Cheung  (09/05/218)
####
#### This script performs a unit test for
#### the book.py.
####
################################################

#################################
#### import packages
#################################
from book import Book
import unittest

#################################
#### unittest class
#################################
class TestBook (unittest.TestCase):

    def setUp (self):

        ''' setup test books at the beginning
            of each test method '''

        pass
        
    @classmethod
    def setUpClass (cls):

        ''' setup test books at the beginning
            of main execution '''

        self.b1     = Book (1, 0) 
        self.b200   = Book (200, 0)
        self.b10000 = Book (10000, 0)

    def tearDown (self):
        pass

    def test_available (self):
        b.available ('B')


#################################
#### execution :)
#################################
if __name__ == '__main__':
    
    unittest.main ()
