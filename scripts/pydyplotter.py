#! /usr/bin/env python

from argparse import ArgumentParser

import matplotlib.pyplot as plt

import pydypackets.PyDyParser as PyDyParser
from pydypackets.PyDyConfig import PyDyConfigParser
from pydypackets.PyDyDevices import device_dict
from pydypackets.PyDyPackets import _id, _cmd, _instr, _len, _val, sum_single_cmd_val


def plot_trends(fr, id=None, instr=3, cmd=30, make_plot=True):
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
    make_plot : boolean
        If False, plotting is skipped.
    
    Returns
    ----------
    plotting_dict : dictionary
        the dictionary storing the lists that would be plotted
    """
    # Get values from PyDyConfigParser:
    cfg = PyDyConfigParser()
    cfg.read()
    subplot_dict = cfg.get_plot_config()
    id_dict = cfg.get_id_to_device_dict()

    # get list of packets, each packet is a list of integers
    packets = PyDyParser.filtering_method(fr, f_id=id, f_instr=instr, \
            f_cmd=cmd, sync_split=True)

    plotting_dict = {}
    for packet in packets:
        if packet[0] != "255":
            xval = [float(packet[0])]
            packet = packet[1:]
        else:
            xval = []
        
        # packet_id = str(packet[_id])
        packet_id = packet[_id]
        
        if packet_id in plotting_dict.keys():
            plotting_dict[packet_id].append(sum_single_cmd_val(packet, cmd, id_dict))
        else:
            plotting_dict[packet_id] = [ sum_single_cmd_val(packet, cmd, id_dict) ]

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
        # If reached the limit of 'plots per window,' then next plots
        # are in a new window.
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

    usage = "usage: %(prog)s [raw-input-file [options] ]\n\n" \
            "This utility creates plots from a PyDyPackets log file. " \
            "Flags are available to filter log files, e.g. to plot only " \
            "specific servos or instructions." \
            "\n\nFiltering includes the ability to automatically split " \
            "sync-write packets into their per-servo commands."

    parser = ArgumentParser(prog='pydyplotter', usage=usage)#, formatter_class=RawTextHelpFormatter)

    #
    parser.add_argument('arglist', nargs='*', default=list(),
            help="Path to a raw input list from pydylogger.")
    parser.add_argument('-s', '--servos', action="store", \
            dest="my_f_id", default=None, help="A single integer " \
            "or set of comma separated integers for servo IDs to keep " \
            "when filtering; e.g. '-s 1,2,3'. Default: %(default)s")
    parser.add_argument('-i', '--instructions', action="store", \
            dest="my_f_instr", default="3", help="A single integer " \
            "or set of comma separated integers for instructions to keep " \
            "when filtering; e.g. '-i 1,2,3'. Default: %(default)s")
    parser.add_argument('-c', '--commands', action="store", \
            dest="my_f_cmd", default="30", help="A single integer " \
            "or set of comma separated integers for commands to keep " \
            "when filtering; e.g. '-c 1,2,3'. Default: %(default)s")
    #

    options = parser.parse_args()
    args = options.arglist
    
    if len(args) == 0:
        print "Command line use requires the name of a file with a packet log."
        print "Use the -h option for more help."
        return
    
    print "Plotting contents of:", args[0]
    with open(args[0], 'r') as fr:
        plot_trends(fr, id=options.my_f_id, \
                instr=options.my_f_instr, cmd=int(options.my_f_cmd))


if __name__ == '__main__':
    main()
