#!/usr/bin/env python

####
#### By Elim Thompson (09/04/2018)
####
#### This script runs the pricer.py solution for
#### the Kinetica job application assignment.
####
#### This script requires a python 3.X. and the
#### following standard python packages:
####  optparse, sys, copy
#### and a class `Book` from book.py
####
#### command to run this script:
####
#### $ python pricer.py --targetsize 200 < cat <input filename> > outfile.log
#### OR
#### $ cat <input filename> | python pricer.py --targetsize 200 > outfile.log
####
###########################################

###########################################
### import packages
###########################################
from optparse import OptionParser
from book import Book
import sys

###########################################
### parse options 
###########################################
usage = "usage: cat <infile> | %prog [--targetsize 200] > outfile.log"
parser = OptionParser (usage=usage)
parser.add_option ('--targetsize', type='int', default=200,
                   help = "number of shares to keep track of.")
(options, args) = parser.parse_args ()

###########################################
### define variables
###########################################
targetsize = options.targetsize
## Verbose is turned off so that no printout
## messages are piped to outfile.
verbose    = 0

###########################################
### function to process each line
###########################################
def process (book, *data):

    ''' process a line of data

        :param book (class `Book`): a given book
        :param data (list)        : [timestamp, add, order, side, price, size] or
                                    [timestamp, reduce, order, size]

        :return message (str): If None, income / expanses remain the same
                               If not None, income / expanses is/are updated
                                            message print to outfile
    '''

    ## first two columns (timestamp and A/R) are ignored
    ## data with 4 elements -> reduce order
    ## data with 6 elements -> add order
    length, args = len (data), data[2:]
    ## data has only 4 or 6 elements
    ## ignore invalid line
    if not length in [4, 6]: return None

    ## print the given line of data
    if verbose: print ('data: {0}'.format (data))

    if length == 6:
        ## data with 6 elements -> add order
        ## *args has 4 elements
        print_income, print_expanse = book.add_order (*args)
    elif length == 4:
        ## data with 4 elements -> reduce order
        ## *args has 2 elements
        print_income, print_expanse = book.reduce_order (*args)

    ## get message (None if nothing is updated
    message = get_message (book, data[0].decode ('utf-8'),
                           print_S=print_income,
                           print_B=print_expanse)
    return message

###########################################
### function to get message
###########################################
def get_message (book, timestamp, print_S=False, print_B=False):

    ''' obtain message for output file if print_S or print_B

        :param book      (class `Book`): a given book
        :param timestamp (str)         : time when income/expanse is updated
        :param print_S   (bool)        : If True, seller sells! Income is updated
        :param print_B   (bool)        : If True, buyer buys! Expanse is updated

        :return message (str): message to be printed in output file
    '''
    
    ## if either income / expanse is updated,
    ## nothing to be printed
    if not print_S and not print_B: return None
    ## print whether action from a 'S'eller or a 'B'uyer
    E = 'S' if print_S else 'B'
    ## get the updated values of money exchange (income / expanse)
    exchange = book.income if print_S else book.expanse
    ## if the value is changed to None, print 'NA'
    ## else the value has two decimal points
    exchange = 'NA' if exchange==None else '{:.2f}'.format (exchange) 
    ## print the array in one string
    return ' '.join ([timestamp, E, exchange])

###########################################
### execution :)
###########################################
if __name__ == '__main__' :

    ## initialize a book instance
    book = Book (targetsize=targetsize,
                 verbose=verbose)

    ## loop through each input line
    for line in sys.stdin:
        # get data from current line
        data = line.split (' ')
        message = process (book, *data)
        
        # write message to new line if updated
        if message: print ('{0}'.format (message))
