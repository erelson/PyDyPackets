#! /usr/bin/env python
import os
from optparse import OptionParser

import PyDyPackets

def parsing_method(stream,f_id=None,f_instr=None,f_len=None):
    """ """
    for line in stream:
        bytes = line.split()
        
        if f_id == None or f_id == str(bytes[_id]
    
    pass

    
def main():
    """Parse command line options
    
    """
    
    usage = "usage: %prog [raw-input-file [options] ]"
    parser = OptionParser(usage)
    
    #
    parser.add_option
    #
    
    (options, args) = parser.parse_args()
    
    with open(args[0], 'r') as fr:
        parsing_method(fr)
    

if __name__ == '__main__':
    main()