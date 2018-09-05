#!/usr/bin/env python

####
#### By Elim Thompson (09/04/2018)
####
#### This contains a class `Book` which
#### keep tracks of the "book".
####
###########################################

from copy import deepcopy

class Book (object):

    ''' This class `Book` is designed to keep track of 
        standing bids and asks in a stock market.
    '''

    def __init__ (self,
                  targetsize=200,
                  verbose=0):
        
        ''' initialize a book instance

            :type  targetsize: int
            :param targetsize: the number of shares

            :type  verbose: int
            :param verbose: If 0, no print out on screen
                            If 1, print info as it goes
        '''

        self._targetsize = targetsize
        self._verbose = verbose

        ## keep track of bids / asks
        self._orders  = {}
        self._income  = {'old':None, 'new':None}
        self._expanse = {'old':None, 'new':None}

    @property
    def income (self):
        return self._income

    @income.getter
    def income (self):
        return self._income['new']

    @property
    def expanse (self):
        return self._expanse

    @expanse.getter
    def expanse (self):
        return self._expanse['new']

    @staticmethod
    def decode (value):

        ''' a statist method to decode a string

            :type  value: a unicode string
            :param value: string to be decoded

            :return value: a decoded string
        '''

        try:
            try:
                return float (value.decode ('utf-8'))
            except:
                return float (value)
        except:
            try: 
                return value.decode ('utf-8')
            except:
                return value

    def available (self, side):

        ''' get current available shares
            from either sellers or buyers

            :type  side: string
            :param side: either 'B' or 'S'

            :return sum: an int
                       : If 'S', check total available shares to be sold
                         If 'B', check total available shares to be bought
        '''

        return int (sum ([ self._orders[order]['size']
                           for order in self._orders
                           if self._orders[order]['side'] == side]))

    def action (self, sell=False, buy=False):

        ''' calculate $$ when action happens, either sell
            or buy can happen.

            If both sell and buy are the same, return None.

            :type  sell: a boolean
            :param sell: If True, sell shares.
 
            :type  buy: a boolean
            :param buy: If True, buy shares.

            :return exchange: a float
                            : either income (sell) or expanse (buy)
        '''

        ## if either sell nor buy, return None
        if sell == buy: return None

        ## step 1: define variables given sell or buy
        side    = 'B'    if sell else 'S'
        reverse = True   if sell else False
        msg     = 'SOLD' if sell else 'BOUGHT'

        ## step 2: sort sellers/buyers by max/min price
        ##         If sell, sell to max buyer available first
        ##         If buy, buy from min seller available first
        orders = {k:v for (k, v) in self._orders.items () if v['side']==side}
        orders = sorted (orders.items (), key = lambda t: t[1]['price'], reverse=reverse)

        ## step 3: calculate income / expanse
        nsize, exchange = 0, 0.
        for order, info in orders:
            # share to sell to this buyer
            size = min (info['size'], self._targetsize - nsize) 
            # $$ from the size and price
            exchange += size * info['price']
            # update available size left
            nsize += size 
            # break when greater than targetsize
            if nsize >= self._targetsize: break

        ## step 4: print info
        self._print_info (msg, exchange)
        return exchange

    def add_order (self, order, side, price, size):

        ''' add an order to the book
    
            :type  order: a string
            :param order: a unique string that subsequent
                          'Reduce Order' messages will use
                          to modify this order

            :type  side: a string
            :param side: a 'B' if this is a buy order (a bid)
                         a 'S' if this is a sell order (an ask)
        
            :type  price: float
            :param price: the limit price of this order
        
            :type  size: int
            :param size: size in shares of this order, when
                         it was initially sent to the market
                         by some stock trader

            :return income: float
                          : total income from selling

            :return expanse: float
                           : total expanse from buying
        '''

        self._print_new_header ('order')
        ## add order
        self._orders[order] = {'side':side, 'price':self.decode (price),
                               'size':self.decode (size)}
        ## print current available shares to buy / sell
        self._print_current ()
        ## if total order from buyer >= targetsize, sell!
        income = self.action (sell=self.available ('B') >= self._targetsize, buy=False)
        ## if total order from seller >= targetsize, buy!
        expanse = self.action (sell=False, buy=self.available ('S') >= self._targetsize)
        ## check if income / expanse are changed from before
        return self.check_update (income, expanse)

    def reduce_order (self, order, size):

        ''' reduce an order from a book

            :type  order: a string
            :param order: a unique string that identifies
                          the order to be reduced.

            :type  size: int
            :param size: amount by which to reduce the size
                         of the order. This is not the new
                         size of the order. If size is equal
                         to or greater than the existing size
                         of the order, the order is removed
                         from the book.
        '''

        self._print_new_header ('reduce')
        ## reduce order by the given size
        self._orders[order]['size'] -= float (self.decode (size))
        ## remove from the book if nothing left
        if self._orders[order]['size'] <= 0.:
            del self._orders[order]
        ## print current status
        self._print_current ()
        return 

    def check_update (self, income, expanse):

        ''' check if income / expanse is updated
            update internal self._income/_expanse

            :type  income: float
            :param income: $$ earned via selling

            :type  expanse: float
            :param expanse: $$ gone via buying

            :return print_income: a boolean
                                : If True, print S in outfile

            :return print_expanse: a boolean
                                 : If True, print B in outfile
        '''

        print_income, print_expanse = False, False
        if not expanse == self._expanse['new']:
            self._expanse['old'] = deepcopy (self._expanse['new'])
            self._expanse['new'] = expanse
            print_expanse = True

        if not income == self._income['new']:
            self._income['old'] = deepcopy (self._income['new'])
            self._income['new'] = income
            print_income = True
        return print_income, print_expanse

    def _print_current (self):

        ''' print current available shares to sell and buy '''

        if self._verbose:
            print ('#### current orders:')
            for order in self._orders:
                print ('#### {0}: {1}'.format (order, self._orders[order]))
            print ('####')
            print ('#### current available to sell from buyers: {0}'.format (self.available ('B')))
            print ('#### current available to buy from sellers: {0}'.format (self.available ('S')))
            print ('####')
            
    def _print_new_header (self, head):

        ''' print the header given an action
            (buying or selling) happens

            :type  head: a string
            :param head: either 'order' for adding order
                         or 'reduce' for reducing order
        '''

        if self._verbose:
            print ('##################################')
            print ('########## new {0:6} ############'.format (head))
            print ('####')

    def _print_info (self, msg, money):

        ''' print the income / expanse of one action
    
            :type  msg: a string
            :param msg: either 'SOLD' or 'BOUGHT'

            :type  money: a float
            :param money: either income or expanse
        '''

        if self._verbose:
            print ('#### {0}: ${1}'.format (msg, money))
