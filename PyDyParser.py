#! /usr/bin/env python

from optparse import OptionParser

import PyDyPackets

def filtering_method(stream,f_id=None,f_instr=None,f_cmd=None):
    """ 
    
    Receives:
    stream - a file stream, e.g. via open('file', 'r')
    (optional:)
    f_id - list/tuple of integers of ID #s to keep
    f_instr - list/tuple of integers of instruction values to keep
    f_cmd - list/tuple of integers of command values to keep
    
    """
    
    f_id = is_list(f_id)
    f_instr = is_list(f_instr)
    f_cmd = is_list(f_cmd)
    
    filtered = list()
    for line in stream:
        bytes = line.split()
        if bytes == []: continue
        
        bytes = [int(x) for x in bytes]
        
        if (f_id == None or bytes[PyDyPackets._id] in f_id) and \
                (f_cmd == None or bytes[PyDyPackets._cmd] in f_cmd) and \
                (f_instr == None or bytes[PyDyPackets._instr] in f_instr):
            filtered.append(bytes)
    
    return filtered

    
def tally_packets(packet_list, tally_by='cmd', **kwargs):
    """Method reports the # of packets of each type
    
    Type depends on the value passed to the tally_by argument
    
    Valid values for tally_by are 'cmd', 'instr', or 'id'.
    
    kwargs that are recognized:
    file : file of packets to read in
    """
    
    dict_tally_by = {'cmd'   : PyDyPackets._cmd, 
                          'instr' : PyDyPackets._instr, 
                          'id'    : PyDyPackets._id
                          }
    
    if tally_by not in dict_tally_by.keys():
        return 0
    
    if 'file' in kwargs:
        packet_list = list()
        with open(kwargs['file'], 'r') as fr:
            for line in fr:
                packet_list.append( [int(x) for x  in line.split()] )
    elif packet_list != None: # I think I forgot a logic case here??
        pass
    else:
        return 0
        
    # Do the tallying
    
    # First create list of the nth byte from each packet
    # try:
    tally_list = [packet[dict_tally_by[tally_by]] for packet in packet_list if packet != [] ]
    tallied_list = tally(tally_list)
    print "Tally results:"
    print "Val:   Instances:"
    for entry in tallied_list:
        print " {0:<7}{1}".format(entry[0],entry[1])
    # catch case where ... ?
    # except:
        # return 2
    
    return tallied_list
    
def is_list(f_thing):
    """Try various ways to assure that we have a list. 
    
    This is just for the heck of it... excessive flexibility...
    """
    
    if f_thing == None: return None
    
    try:
        f_thing = f_thing.split()
        f_thing = [int(x) for x in f_thing]
    except AttributeError: pass
    except: f_thing = None
        
    try: len(f_thing)
    except TypeError: f_thing = [f_thing]
    
    return f_thing
    

def tally(list):
    """Tally frequency of each unique item in a list
    
    Method receives a 1D list and returns a 2D list of with each unique
     element paired with the # of times it appeared in the list (an integer)
    Method is analogous to the Mathematica function Tally[].
    Method adapted from:
    http://bigbadcode.com/2007/04/04/count-the-duplicates-in-a-python-list/
    """
    
    uniqueSet = []
    for item in list:
        if item not in uniqueSet:
            uniqueSet.append(item)
    return [(item, list.count(item)) for item in uniqueSet]
    
    
def main():
    """Parse command line options
    
    """
    
    usage = "usage: %prog [raw-input-file [options] ]"
    parser = OptionParser(usage)
    
    #
    parser.add_option('-s','--servos',action="store", \
            dest="my_f_id",default=None,help="A single integer " \
            "or set of comma separated integers for servo IDs to keep " \
            "when filtering; e.g. '-s 1,2,3'. Default: %default")
    parser.add_option('-i','--instructions',action="store", \
            dest="my_f_instr",default=None,help="A single integer " \
            "or set of comma separated integers for instructions to keep " \
            "when filtering; e.g. '-i 1,2,3'. Default: %default")
    parser.add_option('-c','--commands',action="store", \
            dest="my_f_cmd",default=None,help="A single integer " \
            "or set of comma separated integers for commands to keep " \
            "when filtering; e.g. '-c 1,2,3'. Default: %default")
    parser.add_option('-o','--output',action="store", \
            dest="output",default="filtered_out.txt",help="Specify output " \
            "file for filtered list of packets. Default: %default")
    parser.add_option('-t','--tally',action="store", \
            dest="my_tally_by",default=None,help="Tally filtered packets by " \
            "command (cmd), instruction (instr) or servo ID (id).  E.g.: " \
            "'-t id'. Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    if len(args) == 0:
        print "Command line use requires the name of a file with a packet log."
        print "Use the -h option for more help."
        return
    
    # Do filtering
    with open(args[0], 'r') as fr:
        myfiltered = filtering_method(fr, f_id=options.my_f_id, \
                f_cmd=options.my_f_cmd, f_instr=options.my_f_instr)
    
    # Optionally write filtered results to a new file
    if options.output != '':
        with open(options.output, 'w') as fw:
            for packet in myfiltered:
                fw.write(" ".join([str(x) for x in packet]) + "\n")
        print "Filtered results written to {0}\n".format(options.output)
                
    # Optionally tally packets and report        
    if options.my_tally_by != None:
        tally_packets(myfiltered, tally_by=options.my_tally_by,test=3)
            
    return
    

if __name__ == '__main__':
    main()