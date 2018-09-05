#!/usr/bin/env python

####
#### By Elim Thompson (09/04/2018)
####
#### This script runs the pricer.py solution for
#### the Kinetica job application assignment.
####
#### This script requires a python 3.X.
####
#### command to run this script:
####
#### $ python3 pricer.py --targetsize 200
####                     --verbose 0
####                    (--test if use test file)
####
###########################################

###########################################
### import packages
###########################################
from optparse import OptionParser
from book import Book
import os, gzip, time

###########################################
### parse options 
###########################################
usage = "usage: %prog [--targetsize 200 --verbose 0 (--test)]"
parser = OptionParser (usage=usage)
parser.add_option ('--targetsize', type='int', default=200,
                   help = "number of shares to keep track of.")
parser.add_option ('--verbose', type='int', default=0,
                   help = "If 0, no print out; If 1, print details")
parser.add_option ('--test', action='store_true', default=False,
                   help = "If --test, use test input file instead")
(options, args) = parser.parse_args ()

targetsize = options.targetsize
verbose    = options.verbose
test       = options.test

###########################################
### define variables
###########################################
## this directory
thisdir = os.path.dirname (os.path.abspath (__file__)) + '/'

###########################################
### function to load input file
###########################################
def load_input ():
    ## define input files
    infile  = 'Pricer/test.in.gz' if test else \
              'Pricer/pricer.in.gz'
    ## read infile - pricer.in.gz
    with gzip.open (infile, 'rb') as f:
        intxt = f.read ()
    f.close ()
    ## return individual lines in a list
    return intxt.decode ('utf-8').split ('\n')

###########################################
### function to process each line
###########################################
def process (*data):

    ''' process a line of data

        :type  data: list of information
        :param data: (timestamp, add, order, side, price, size) or
                     (timestamp, reduce, order, size)

        :return outline: a string
                outline: If None, no action
                         If not None, action happens
    '''

    length, args = len (data), data[2:]
    message = None
    if length == 6:
        print_income, print_expanse = book.add_order (*args)
        message = get_message (data[0].decode ('utf-8'),
                               print_S=print_income,
                               print_B=print_expanse)
    elif length == 4:
        book.reduce_order (*args) 
    else:
        print ("invalid line: {0}".format (data))
    return message

###########################################
### function to get message
###########################################
def get_message (timestamp, print_S=False, print_B=False):

    if not print_S and not print_B: return None
    E = 'S' if print_S else 'B'
    exchange = book.income if print_S else book.expanse
    return ' '.join ([timestamp, E, str (exchange), '\n'])

###########################################
### execution :)
###########################################
if __name__ == '__main__' :

    ## define output file
    outfile = thisdir + 'Pricer/elimtest.out' if test else \
              thisdir + 'Pricer/elim.out'

    ## initialize a book instance
    book = Book (targetsize=targetsize,
                 verbose=verbose)

    ## open outfile
    with open (outfile, 'wb') as f:
        
        ## loop through each input line
        for line in load_input ():
            # get data from current line
            data = line.split (' ')
            message = process (*data)

            # write message to new line if updated
            if message: f.write (message)

    ## close outfile
    f.close ()
