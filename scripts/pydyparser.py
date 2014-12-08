#! /usr/bin/env python

from argparse import ArgumentParser, RawTextHelpFormatter
from StringIO import StringIO
from textwrap import TextWrapper

from pydypackets.PyDyParser import filtering_method, tally_packets
from pydypackets.PyDyPackets import translate_packet
from pydypackets.PyDyConfig import PyDyConfigParser

    
def do_filtering(options, args, id_dict):
    """

    Parameters
    ----------
    options : ArgumentParser.parse_args() output
        Contains options from commandline input
    args : list of raw strings
        Contains arguments from commandline input
    id_dict : dictionary

    """
    # Parse input and do filtering.
    # myfiltered is a list of packets; each pack is a list of integers.
    if options.quick:
        quickstream = StringIO(' '.join(args[0:]))
        myfiltered = filtering_method(quickstream, f_id=options.my_f_id, \
                f_instr=options.my_f_instr, f_cmd=options.my_f_cmd, \
                sync_split=options.sync_split)
    else:
        with open(args[0], 'r') as fr:
            myfiltered = filtering_method(fr, f_id=options.my_f_id, \
                    f_instr=options.my_f_instr, f_cmd=options.my_f_cmd, \
                    sync_split=options.sync_split)
    
    # Optionally write filtered results to a new file
    if options.output != '':
        if options.quick:
            print translate_packet(myfiltered[0], id_dict, includetime=options.timestamp)
        elif len(myfiltered):
            with open(options.output, 'w') as fw:
                # either translated output
                if options.translate:
                    for packet in myfiltered:
                        packet = translate_packet(packet, id_dict, \
                                includetime=options.timestamp)
                        fw.write("\t".join(packet) + "\n")
                # or raw integer output; float timestamp included if exists
                else:
                    for packet in myfiltered:
                        fw.write(" ".join([str(x) for x in packet]) + "\n")
            print "Filtered results written to {0}\n".format(options.output)
        else:
            print "No packets satisfied the filters specified."
    
    # Optionally tally packets and report
    if options.my_tally_by != None:
        tally_packets(myfiltered, tally_by=options.my_tally_by)
    
    return


def main():
    """Parse command line options
    
    """
    usage = "usage: %(prog)s [raw-input-file [options] ]\n" \
            "Program will filter and/or translate supplied raw packets.\n"
    parser = ArgumentParser(prog='pydyparser', usage=usage,
                            formatter_class=RawTextHelpFormatter)

    tw = TextWrapper()
    mywrap = lambda x: "\n".join(tw.wrap(x))
    tw.width = 80 - 25
    quicktext = "\n".join(["\n".join(tw.wrap(_)) for _ in (
            "Arg(s) will be concatenated and treated as "
            "a single packet and then parsed. Input should be space-delimited "
            "bytes. 0xff, 255, and \\xff styles are all supported. "
            "If using the latter, space delimiting is optional, but you must "
            "wrap the sequence of bytes in quotes "
            "(or escape the backslashes).\n\n"
            "Example usage:"
            "\n$ pydyparser -q 255 255 12 7 3 30 0 2 0 2 195"
            "\n$ pydyparser -q 0xFF 0xFF 0x0C 0x07 0x03 0x1E 0x00 0x02 0x00 0x02 0xC3"
            "\n$ pydyparser -q \"\\xFF\\xFF\\x0C\\x07\\x03\\x1E\\x00\\x02\\x00\\x02\\xC3\""
            "\n$ pydyparser -q \"\\xFF \\xFF \\x0C \\x07 \\x03 \\x1E \\x00 \\x02 \\x00 \\x02 \\xC3\""
            "\n\nThese all produce output:\n"
            " ['ID: 12', 'write data', 'GOAL_POSITION_L       ', 'Val:     512', "
            "'GOAL_SPEED_L', 'Val:     512', 'invalid checksum c3 (actual c9)']").splitlines()])

    #
    parser.add_argument('arglist', nargs='*', default=list(),
            help=mywrap("Path to a file to parse/translate, or list of bytes "
            "to parse/translate if using -q flag."))
    parser.add_argument('-q', '--quick', action="store_true", dest="quick",
            default=False, help=quicktext)
    parser.add_argument('-s', '--servos', action="store",
            dest="my_f_id", default=None,
            help=mywrap("A single integer "
            "or set of comma separated integers for servo IDs to keep "
            "when filtering; e.g. '-s 1,2,3'.\nDefault: %(default)s"))
    parser.add_argument('-i', '--instructions', action="store",
            dest="my_f_instr", default=None, help=mywrap("A single integer "
            "or set of comma separated integers for instructions to keep "
            "when filtering; e.g. '-i 1,2,3'.\nDefault: %(default)s"))
    parser.add_argument('-c', '--commands', action="store",
            dest="my_f_cmd", default=None, help=mywrap("A single integer "
            "or set of comma separated integers for commands to keep "
            "when filtering; e.g. '-c 1,2,3'.\nDefault: %(default)s"))
    parser.add_argument('-o', '--output', action="store",
            dest="output", default="filtered_out.txt", help=mywrap("Specify "
	    "output file for filtered list of packets. (do `-o ''` to prevent "
	    "output creation.) Default: %(default)s"))
    parser.add_argument('-t', '--translate', action="store_true",
            dest="translate", default=False, help=mywrap("Write filtered "
	    "packets in human-readable form.\nDefault: %(default)s"))
    parser.add_argument('--time', action="store_true",
            dest="timestamp", default=None, help=mywrap("Appends timestamps "
	    "to end of each translated packet (if timestamps exist). "
	    "Default: %(default)s"))
    parser.add_argument('-T', '--Tally', action="store",
            dest="my_tally_by", default=None, help=mywrap("Tally filtered "
	    "packets by command (cmd), instruction (instr) or servo ID (id). "
	    "E.g.: '-T id'. Default: %(default)s"))
    parser.add_argument('-S', '--SyncWrite', action="store_true",
            dest="sync_split", default=None, help=mywrap("Split up sync-write "
	    "packets when filtering to look for contents satisfying other "
	    "criteria. Can also be used just to create individual packets. "
            "Default: %(default)s"))
    #
    
    options = parser.parse_args()
    args = options.arglist
    
    if len(args) == 0:
        print "Command line use requires the name of a file with a packet " \
                "log. (Or a string of bytes if using --quick option.)\n" \
                "Use the -h option for more help."
        return

    cfg = PyDyConfigParser()
    cfg.read()
    __, __, __, __, itit = cfg.get_params()
    id_dict = cfg.get_id_to_device_dict()

    if options.timestamp is None:
        options.timestamp = itit

    do_filtering(options, args, id_dict)
    return
    

if __name__ == '__main__':
    main()
