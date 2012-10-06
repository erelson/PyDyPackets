#! /usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt

from optparse import OptionParser

import PyDyParser
from PyDyPackets import _id, _cmd, _instr, _len, _val, sum_vals

dict_subplot= { 0: 311, 1: 312, 2: 313 }

def plot_trends(fr, id=None, instr=3, cmd=30):
    """
    """
    
    # get list of packets, each packet is a list of integers
    packets = PyDyParser.filtering_method(fr, f_id=id, f_instr=instr, f_cmd=cmd)
    
    plotting_dict = {}
    for packet in packets:
        if packet[_id] in plotting_dict.keys():
            plotting_dict[packet[_id]].append(sum_vals(packet))
        else:
            plotting_dict[packet[_id]] = [ sum_vals(packet) ]
            
    fignum = 1
    plt.figure(1)
    cnt = 0;
    for key in plotting_dict.keys():
        print key
        if cnt == 3:
            fignum += 1
            plt.figure(fignum)
            cnt = 0
        print cnt
        plt.subplot(dict_subplot[cnt])
        plt.plot(plotting_dict[key])
        plt.title(key)
        
        cnt += 1
        
    plt.show()
    

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
            dest="my_f_instr",default="3",help="A single integer " \
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
    
    with open(args[0], 'r') as fr:
        plot_trends(fr)

if __name__ == '__main__':
    main()