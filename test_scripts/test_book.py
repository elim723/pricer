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

        self.b1     = Book (1, 0) 
        self.b200   = Book (200, 0)
        self.b10000 = Book (10000, 0)

    def tearDown (self):
        pass

    def test_available (self):

        ''' test available () using self.b1 only
            because available () is independent
            of targetsize
        '''

        ## add an order 'nmlt'
        self.b1._orders['nmlt'] = {'side':'S', 'price':43.99, 'size':300}
        self.assertEqual (self.b1.available ('S'), 300)
        self.assertEqual (self.b1.available ('B'), 0)
        ## add another order 'qmlt'
        self.b1._orders['qmlt'] = {'side':'B', 'price':43.96, 'size':3}
        self.assertEqual (self.b1.available ('S'), 300)
        self.assertEqual (self.b1.available ('B'), 3)
        ## reduce an order 'nmlt'
        del self.b1._orders['nmlt']
        self.assertEqual (self.b1.available ('S'), 0)
        self.assertEqual (self.b1.available ('B'), 3)
        ## add an order 'smlt'
        self.b1._orders['smlt'] = {'side':'B', 'price':43.96, 'size':3}
        self.assertEqual (self.b1.available ('S'), 0)
        self.assertEqual (self.b1.available ('B'), 6)

    def test_exchange (self):

        ''' test exchange () '''
    
        ## test if both sell and buy are the same
        self.assertIsNone (self.b1.exchange (sell=True, buy=True))
        self.assertIsNone (self.b1.exchange (sell=False, buy=False))

        ## test if seller/buyer gets to sell/buy for each of the three target sizes
        for index, b in enumerate ([self.b1, self.b200, self.b10000]):
            ## add a new order 'a' from a buyer
            b._orders['a'] = {'side':'B', 'price':43.99, 'size':300}
            expected_income = 43.99
            ## add a new order 'aa' from a seller
            b._orders['aa'] = {'side':'S', 'price':43.99, 'size':50}
            expected_expanse = 43.99
            if index > 0:
                ## add another new order 'b' from a second buyer
                b._orders['b'] = {'side':'B', 'price':51.06, 'size':100}
                expected_income = 100*51.06+100*43.99
                ## add another new order 'bb' from a second seller
                b._orders['bb'] = {'side':'S', 'price':51.06, 'size':200}
                expected_expanse =  50*43.99+150*51.06
            if index > 1:
                ## add another new order 'c' from a third buyer
                b._orders['c'] = {'side':'B', 'price':38.45, 'size':20000}
                expected_income = 100*51.06+300*43.99+(10000-400)*38.45
                ## add another new order 'cc' from a third seller
                b._orders['cc'] = {'side':'S', 'price':38.45, 'size':30}
                expected_expanse = None
            ## check if any selling/buying actions happen
            sell = b.available ('B') >= b._targetsize
            buy  = b.available ('S') >= b._targetsize
            ## check the answer from b.exchange () and expected exchange
            self.assertEqual (b.exchange (sell=sell, buy=False), expected_income)
            self.assertEqual (b.exchange (sell=False, buy=buy), expected_expanse)

    def test_action (self):

        ''' test action ()'''

        ## test if any updates on income / expanses
        for index, b in enumerate ([self.b1, self.b200, self.b10000]):
            ## add a new order 'a' from a buyer
            b._orders['a'] = {'side':'B', 'price':43.99, 'size':300}
            income_bool = True
            ## add a new order 'aa' from a seller
            b._orders['aa'] = {'side':'S', 'price':43.99, 'size':50}
            expanse_bool = True
            if index > 0:
                ## add another new order 'b' from a second buyer
                b._orders['b'] = {'side':'B', 'price':51.06, 'size':100}
                income_bool = True
                ## add another new order 'bb' from a second seller
                b._orders['bb'] = {'side':'S', 'price':51.06, 'size':200}
                expanse_bool = True
            if index > 1:
                ## add another new order 'c' from a third buyer
                b._orders['c'] = {'side':'B', 'price':38.45, 'size':20000}
                income_bool = True
                ## add another new order 'cc' from a third seller
                b._orders['cc'] = {'side':'S', 'price':38.45, 'size':30}
                expanse_bool = False
            ## check the answer from b.action () and expected exchange bools
            self.assertEqual (b.action (), (income_bool, expanse_bool))

    def test_add_order (self):

        ''' test add_order (order, side, price, size) '''

        ## raw data lines
        datas = ['28800562 A c B 44.10 100',
                 '28800758 A d B 44.18 157',
                 '28800773 A e S 44.38 100']
        ## split data lines
        datas = [data.split (' ') for data in datas]

        ## test if any updates on income / expanses as data goes
        for index, b in enumerate ([self.b1, self.b200, self.b10000]):

            # first data line
            income_bool, expanse_bool = True, False
            if index > 0: income_bool, expanse_bool = False, False
            self.assertEqual (b.add_order (*datas[0][2:]), (income_bool, expanse_bool))

            # first two data lines
            income_bool, expanse_bool = True, False
            if index > 1: income_bool, expanse_bool = False, False
            self.assertEqual (b.add_order (*datas[1][2:]), (income_bool, expanse_bool))

            # all three data lines
            income_bool, expanse_bool = False, True
            if index > 0: income_bool, expanse_bool = False, False
            self.assertEqual (b.add_order (*datas[2][2:]), (income_bool, expanse_bool))

    def test_reduce_order (self):

        ''' test reduce_order (order, side) '''

        ## raw data lines
        datas = ['28800562 A c B 44.10 100',
                 '28800758 A d B 44.18 157',
                 '28800765 R c 100',
                 '28800773 A e S 44.38 100',
                 '28800765 R d 157'        ]
        ## split data lines
        datas = [data.split (' ') for data in datas]

        ## test if any updates on income / expanses as data goes
        for index, b in enumerate ([self.b1, self.b200, self.b10000]):

            # first two data lines
            b.add_order (*datas[0][2:])
            b.add_order (*datas[1][2:])
            
            # first third data line
            income_bool, expanse_bool = False, False
            if index == 1: income_bool, expanse_bool = True, False
            self.assertEqual (b.reduce_order (*datas[2][2:]), (income_bool, expanse_bool))

            # first four data lines
            b.add_order (*datas[3][2:])

            # include all data lines
            income_bool, expanse_bool = True, False
            if index > 0: income_bool, expanse_bool = False, False
            self.assertEqual (b.reduce_order (*datas[4][2:]), (income_bool, expanse_bool))
            
#################################
#### execution :)
#################################
if __name__ == '__main__':
    
    unittest.main ()
