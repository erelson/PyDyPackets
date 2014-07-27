#! /usr/bin/env python

from optparse import OptionParser
    
from pydypackets.PyDyParser import filtering_method, tally_packets
from pydypackets.PyDyPackets import translate_packet
from pydypackets.PyDyConfig import include_timestamp_in_translate as itit

    
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
    parser.add_option('-t','--translate',action="store_true", \
            dest="translate",default=False,help="Write filtered packets in " \
            "human-readable form. Default: %default")
    parser.add_option('--time',action="store_true", \
            dest="timestamp",default=itit,help="Appends timestamps to end of " \
            "each translated packet (if timestamps exist). Default: %default")
    parser.add_option('-T','--Tally',action="store", \
            dest="my_tally_by",default=None,help="Tally filtered packets by " \
            "command (cmd), instruction (instr) or servo ID (id).  E.g.: " \
            "'-T id'. Default: %default")
    parser.add_option('-S','--SyncWrite',action="store_true", \
            dest="sync_split",default=None,help="Split up sync-write packets " \
            "when filtering to look for contents satisfying other criteria. " \
            "Can also be used just to create individual packets. " \
            "Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    if len(args) == 0:
        print "Command line use requires the name of a file with a packet log."
        print "Use the -h option for more help."
        return
    
    # Do filtering
    #  myfiltered is a list of packets; each pack is a list of integers.
    with open(args[0], 'r') as fr:
        myfiltered = filtering_method(fr, f_id=options.my_f_id, \
                f_instr=options.my_f_instr, f_cmd=options.my_f_cmd, \
                sync_split=options.sync_split)
    
    # Optionally write filtered results to a new file
    if options.output != '':
        if len(myfiltered):
            with open(options.output, 'w') as fw:
                if options.translate: # translated output
                    for packet in myfiltered:
                        packet = translate_packet(packet, \
                                includetime=options.timestamp)
                        fw.write("\t".join(packet) + "\n")
                else: # raw integer output; float timestamp included if exists
                    for packet in myfiltered:
                        fw.write(" ".join([str(x) for x in packet]) + "\n")
            print "Filtered results written to {0}\n".format(options.output)
        else:
            print "No packets satisfied the filters specified."
    
    # Optionally tally packets and report
    if options.my_tally_by != None:
        tally_packets(myfiltered, tally_by=options.my_tally_by)
    
    return
    

if __name__ == '__main__':
    main()
