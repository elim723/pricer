#!/usr/bin/env python

####
#### By Elim Cheung  (09/05/218)
####
#### This script performs a unit test for
#### the pricer.py.
####
################################################

#################################
#### import packages
#################################
from pricer import process
from book import Book
import unittest

#################################
#### define global variables
#################################
b1   = Book (1, 0)
b200 = Book (200, 0)

datas = ['28800538 A b S 44.26 100',
         '28800562 A c B 44.10 100',
         '28800744 R b 100'        ,
         '28800758 A d B 44.18 157',
         '28800773 A e S 44.38 100',
         '28800796 R d 157'        ]

#################################
#### unittest class
#################################
class TestPricer (unittest.TestCase):

    def test_process (self):

        ''' test process () '''
        
        ## test books with different target sizes
        for bdex, b in enumerate ([b1, b200]):
            ## test with datas
            for ddex, data in enumerate (datas):
                msg = '28800758 S 8832.56' if bdex==1 and ddex==3 else \
                      '28800796 S NA'      if bdex==1 and ddex==5 else \
                      '28800538 B 44.26'   if bdex==0 and ddex==0 else \
                      '28800562 S 44.10'   if bdex==0 and ddex==1 else \
                      '28800744 B NA'      if bdex==0 and ddex==2 else \
                      '28800758 S 44.18'   if bdex==0 and ddex==3 else \
                      '28800773 B 44.38'   if bdex==0 and ddex==4 else \
                      '28800796 S 44.10'   if bdex==0 and ddex==5 else \
                      None
                ## check expected answer from process ()
                self.assertEqual (process (b, *data.split (' ')), msg)

#################################
#### execution :)
#################################
if __name__ == '__main__':
    
    unittest.main ()
