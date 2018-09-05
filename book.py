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

            :param targetsize (int): the number of shares

            :param verbose (int): If 0, no print out on screen
                                  If 1, print info as it goes
        '''

        self._targetsize = targetsize
        self._verbose = verbose

        ## keep track of bids / asks
        ## and money exchange in the market
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

            :param value (unicode): string to be decoded

            :return value (str): decoded string
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

        ''' get current available shares from either sellers or buyers

            :param side (str): either 'B' for buy or 'S' for sell

            :return sum (int): If 'S', total available shares to be sold
                               If 'B', total available shares to be bought
        '''

        return int (sum ([ self._orders[order]['size']
                           for order in self._orders
                           if self._orders[order]['side'] == side]))

    def exchange (self, sell=False, buy=False):

        ''' calculate $$ when an exchange happens, either sell
            or buy can happen.

            If both sell and buy are the same, return None.
            This function only deals with one exchange.

            :param sell (bool): If True, sell shares.
            :param buy  (bool): If True, buy shares.

            :return exchange (float): either income (sell) or expanse (buy)
        '''

        ## if either sell nor buy, return None
        ## (only one exchange is dealt here)
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
            # share to sell to this buyer or to buy from this seller
            size = min (info['size'], self._targetsize - nsize) 
            # $$ from the size and price
            exchange += size * info['price']
            # update available size left
            nsize += size 
            # print 
            self._print_calculation (order, info, size, nsize)
            # break when greater than targetsize
            if nsize >= self._targetsize: break

        ## step 4: print SOLD / BOUGHT at what value
        self._print_exchange (msg, exchange)
        return exchange

    def action (self):

        ''' perform selling / buying when needed
            update income / expanse as it goes

            :return updated_income  (bool): If True, self._income is updated
            :return updated_expanse (bool): If True, self._expanse is updated
        '''

        ## if total order from buyer >= targetsize, sell!
        income = self.exchange (sell=self.available ('B') >= self._targetsize, buy=False)
        ## if total order from seller >= targetsize, buy!
        expanse = self.exchange (sell=False, buy=self.available ('S') >= self._targetsize)

        ## update if income / expanse are changed from before
        updated_income = self._update ('income', income)
        updated_expanse = self._update ('expanse', expanse)
        return updated_income, updated_expanse

    def add_order (self, order, side, price, size):

        ''' add an order to the book
    
            :param order (str)  : a unique string that subsequent 'Reduce Order'
                                  messages will use to modify this order

            :param side  (str)  : a 'B' if this is a buy  order (a bid)
                                  a 'S' if this is a sell order (an ask)
        
            :param price (float): the limit price of this order
        
            :param size  (int)  : size in shares of this order, when it was
                                  initially sent to the market by some stock trader

            :return updated_income  (bool): If True, income is updated by this order

            :return updated_expanse (bool): If True, expanse is updated by this order
        '''

        self._print_header ('order')
        ## add order
        self._orders[order] = {'side':side, 'price':self.decode (price),
                               'size':self.decode (size)}
        ## print current available shares
        self._print_current_shares ()
        ## perform any action after the order is added
        updated_income, updated_expanse = self.action ()
        return updated_income, updated_expanse

    def reduce_order (self, order, size):

        ''' reduce an order from a book

            :param order (str): a unique string that identifies
                                the order to be reduced.

            :param size  (int): amount by which to reduce the size of the order. This
                                is not the new size of the order. If size is equal to
                                or greater than the existing size of the order, the
                                order is removed from the book.

            :return updated_income  (bool): If True, income is updated by this order

            :return updated_expanse (bool): If True, expanse is updated by this order
        '''

        self._print_header ('reduce')
        ## reduce order by the given size
        self._orders[order]['size'] -= float (self.decode (size))
        ## remove from the book if nothing left
        if self._orders[order]['size'] <= 0.:
            del self._orders[order]
        ## print current available shares
        self._print_current_shares ()
        ## perform any action after the order is added
        updated_income, updated_expanse = self.action ()
        return updated_income, updated_expanse

    def _update (self, exchangetype, exchange):

        ''' check if income / expanse is updated
            update internal self._income/_expanse

            :param exchangetype (str)  : either 'income' or 'expanse'
            :param exchange     (float): $$ either income or expanse

            :return print_exchange (bool): If True, exchangetype is
                                           updated and print = True
        '''

        ## default = nothing is changed
        print_exchange = False
        ## define the variable to be changed based on income / expanse
        container = eval ('self._' + exchangetype)
        ## check if current exchange is the same as before
        same = exchange == container['new']
        ## double check if they are the same after rounding
        ## (this extra step needed if both current and new are not None
        if exchange and container['new']:
            same = round (exchange, 10) == round (container['new'], 10)
        ## update if not the same
        if not same:
            # move 'new' value to old
            container['old'] = deepcopy (container['new'])
            # replace 'new' value to current value
            container['new'] = exchange
            # flag: this value is changed
            print_exchange = True
            # print what is being updated to what value
            self._print_update (exchangetype, container)
        return print_exchange

    def _print_update (self, exchangetype, container):

        ''' print what is updated to what value '''

        if self._verbose:
            print ('#### {0} is updated !!!'.format (exchangetype))
            print ('####     from {0} ...'.format (container['old']))
            print ('####     to   {0} ...'.format (container['new']))

    def _print_calculation (self, order, info, size, nsize):

        ''' print information of a given order in a given exchange '''
        
        if self._verbose:
            print ('#### +---- {0}'.format (order))
            print ('####     --- info size, price: {0}, {1}'.format (info['size'], info['price']))
            print ('####     --- size can be sold/bought: {0}'.format (size))
            print ('####     --- nsize: {0}'.format (nsize))

    def _print_current_shares (self):

        ''' print current available shares to sell and buy '''

        if self._verbose:
            print ('#### current orders:')
            for order in self._orders:
                print ('####     {0}: {1}'.format (order, self._orders[order]))
            print ('####')
            print ('#### current available to sell from buyers: {0}'.format (self.available ('B')))
            print ('#### current available to buy from sellers: {0}'.format (self.available ('S')))
            print ('####')
            print ('#### current old, new self._income : {0}, {1}'.format (self._income['old'],
                                                                           self._income['new'] ))
            print ('#### current old, new self._expanse: {0}, {1}'.format (self._expanse['old'],
                                                                           self._expanse['new'] ))
            print ('####')
        
    def _print_header (self, head):

        ''' print the header given a line of data '''

        if self._verbose:
            print ('##################################')
            print ('########## new {0:6} ############'.format (head))
            print ('####')

    def _print_exchange (self, msg, money):

        ''' print the income / expanse of a given exchange
    
            :param msg   (str)  : either 'SOLD' or 'BOUGHT'
            :param money (float): either income or expanse
        '''

        if self._verbose:
            print ('#### {0}: ${1}'.format (msg, money))
