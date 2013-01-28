#! /usr/bin/env python

from PyDyConfig import id_dict
from PyDyDevices import device_dict

import matplotlib.pyplot as plt

from optparse import OptionParser

import PyDyParser
from PyDyPackets import _id, _cmd, _instr, _len, _val, sum_single_cmd_val

from PyDyConfig import dict_subplot

def plot_trends(fr, id=None, instr=3, cmd=30, subplot_dict=dict_subplot, \
                    make_plot=True):
    """A file stream of packets is filtered and plotted
    
    The packet stream is stored as a dictionary of lists, with each list
    corresponding to a servo ID.
    
    Parameters
    ----------
    fr : file stream
        e.g. via ``open('file', 'r')``
    (optional)
    id : list/tuple of integers
        ID #s to keep
    instr : list/tuple of integers
        instruction values to keep
    cmd : integer
        command value to keep
    subplot_dict : dictionary
        A custom dictionary with keys starting from 0.  Each key
        corresponds with a subplot specification.  Typically, these defines 
        a 3-digit subplot value, where digits are (1) # columns; (2) # rows;
        (3) plotnum. Plotnum goes row by row, filling columns of each row.
        You can specify this dictionary when calling plot_trends, or just 
        modify dict_subplot in PyDyPlotter.py.
        See also:
        http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.subplot
    make_plot : boolean
        If False, plotting is skipped.
    
    Returns
    ----------
    plotting_dict : dictionary
        the dictionary storing the lists that would be plotted
    """
    
    # get list of packets, each packet is a list of integers
    packets = PyDyParser.filtering_method(fr, f_id=id, f_instr=instr, \
            f_cmd=cmd, sync_split=True)
    
    plotting_dict = {}
    for packet in packets:
        if packet[0] != "255":
            xval = [float(packet[0])]
            packet = packet[1:]
        else: xval = []
            
        # packet_id = str(packet[_id])
        packet_id = packet[_id]
        
        if packet_id in plotting_dict.keys():
            plotting_dict[packet_id].append(sum_single_cmd_val(packet, cmd))
        else:
            plotting_dict[packet_id] = [ sum_single_cmd_val(packet, cmd) ]
    
    # plotkeys is the list (and order) of plots to make
    if id is None:
        plotkeys = plotting_dict.keys()
    else:
        plotkeys = PyDyParser._is_list(id)
        # This preserves the user-specified order, but tosses IDs that weren't
        # in the filtered packets.
        plotkeys = [x for x in plotkeys if x in plotting_dict.keys()]
        
    # Generate the plots
    fignum = 1
    plt.figure(1)
    cnt = 0;
    for key in plotkeys:
        # If reached the limit of plots/window
        if cnt == len(subplot_dict.keys()):
            fignum += 1
            plt.figure(fignum)
            cnt = 0
        
        plt.subplot(subplot_dict[cnt])
        plt.plot(plotting_dict[key])
        plt.title("{1} ID: {0}".format(key, id_dict[key]))
        
        cnt += 1
        
    if make_plot:
        plt.show()
    
    # script pauses until plot window is closed.
    
    return plotting_dict
    

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
            dest="my_f_cmd",default="30",help="A single integer " \
            "or set of comma separated integers for commands to keep " \
            "when filtering; e.g. '-c 1,2,3'. Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    if len(args) == 0:
        print "Command line use requires the name of a file with a packet log."
        print "Use the -h option for more help."
        return
    
    with open(args[0], 'r') as fr:
        plot_trends(fr, id=options.my_f_id, \
                instr=options.my_f_instr, cmd=int(options.my_f_cmd))

if __name__ == '__main__':
    main()