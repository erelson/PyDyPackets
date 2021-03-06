#! /usr/bin/env python

from optparse import OptionParser

from pydypackets.PyDyConfig import PyDyConfigParser
from pydypackets.PyDyDevices import device_dict


# Global indices for getting bytes from packets;
# I'm doing this so I can easily toss the FF FF leading bytes if desired...
# 0 and 1 are the leading 0xFF bytes
_id = 2
_len = 3     # note length is N + 3 where N is # of parameter bytes
_instr = 4
_cmd = 5     # address to start writing or reading data at
_val = 6
_synclen = 6 # where the length of subpackets is specified for sync-write
_syncval = 7 # where the first subpacket begins for sync-writes
_readcmd = 5 # address to start reading data at
_readlen = 6 # number of registers read-data packet is requesting

#           #instr #name          #num param bytes plus a cmd byte
dictInstr = {0x00: ["status OK;", "0 "],
             0x01: ["ping      ", "0 "],
            #0x01 is also input voltage error
             0x02: ["read data ", "2 "],
            #0x02 is also angle limit error
             0x03: ["write data", "2+"],
             0x04: ["reg write ", "2+"],
            #0x04 is also overheating error
             0x05: ["action    ", "0 "],
             0x06: ["reset     ", "0 "],
            #0x08 is range error bit
            #0x10 is checksum error bit
            #0x20 is overload error bit
            #0x40 is instruction error bit
            #0x80 is an unused error bit
             0x83: ["sync write", "4+"]
            }

            
def show_instr():
    """ """
    print ""
    print "In command line arguments (-i), enter the numeric value in column 3."
    print "\nInstruction:     Value:       # of parameters  "
    for key in dictInstr:
        print " {0:15}0x{1:<4X}{1:<4}{2:>12}".format( \
                dictInstr[key][0],key,dictInstr[key][1])
        
    return
    
    
def show_cmd(myid=None):
    """ """
    # Get values from PyDyConfigParser:
    cfg = PyDyConfigParser()
    cfg.read()
    __, __, default_device_type, __, __ = cfg.get_params()
    
    dictCmd = device_dict[default_device_type]
    print "\nPrinting the command set for default device ({0}):".format( \
            default_device_type)
    
    print ''
    print "In command line arguments (-c), enter the number value in column 2"
    print "\nCommand:                  Value:        valid range"
    for key in dictCmd:
        if dictCmd[key][0][:3] != "BAD": # Suppress BAD entries
            print "  {0:24}0x{1:<4X}{1:<4}{2:>8}".format( \
                    dictCmd[key][0], key, dictCmd[key][1])
    
    return

def is_bad_packet(byte_packet):
    """Return true if a packet is invalid
    
    TODO: Determine more conditionals/defintions of bad packets.
    
    Parameters
    -----------
    byte_packet : list of integers
        List of bytes in a packet, including FF FF.
        
    Returns
    -------
    boolean
    """
    return len(byte_packet) < _cmd

    
def sum_single_cmd_val(byte_packet, cmd, id_dict):
    """Sum value bytes by shifting the higher bytes as needed
    
    Parameters
    -----------
    byte_packet : list of integers
        List of bytes in a packet, including FF FF.
    cmd : integer
        Desired command address to take data value from
        
    Returns
    -------
    val : integer
        Sum of low and high bytes,
    """
    # Skip any timestamp passed
    if byte_packet[0] != 255:
        byte_packet = byte_packet[1:]
        
    dictCmd = device_dict[id_dict[byte_packet[_id]]]
    
    # Find offset and number of bytes to pass to sum_vals
    # Offset is limited by # of val bytes in packet,
    #  and # of value bytes for cmd
    offset = 0
    while ( cmd > offset + byte_packet[_cmd] ) \
            and ( offset < byte_packet[_len] - 3 ):
        offset += 1
    # The number of bytes is limited by either the cmd, or the packet length
    val_length = dictCmd[cmd][1]
    if val_length + offset > (byte_packet[_len] - 3):
        val_length = (byte_packet[_len] - 3) - offset
        
    val = sum_vals(byte_packet[offset+_val:offset+_val+val_length])
    
    return val
    
    
def sum_vals(bytes):
    """Sum value bytes by shifting the higher bytes as needed
    
    Parameters
    ----------
    bytes : list of integers
        List of value bytes (not a complete packet)
        
    Returns
    -------
    val : integer
        Sum of low and high bytes,
    """
    val = 0
    for i in xrange(len(bytes)):
        val += bytes[i]<<(8*i)
        
    return val
    
    
def vals_split_and_translate(vals, mycmd, id_dict, myid=None):
    """Return translated list of single or multiple commands
    
    Parameters
    ----------
    vals : list of integers
        List of value bytes in the packet
    mycmd : integer
        Register at which to start reading bytes
    myid : integer, optional
        ID of servo for values being translated. Filters packets to only
        those for this ID.
    
    Returns
    -------
    cmdList : list of strings
        List of commands and values
    """
    dictCmd = device_dict[id_dict[myid]]
    
    cnt = 0
    cmdList = list()
    try:
        while cnt < len(vals):
            # handle last byte in vals
            if cnt + 1 == len(vals):
                cmdList += [dictCmd[mycmd+cnt][0], "Val:{0:8}".format( \
                        sum_vals(vals[cnt:cnt+1]) ) ]
                cnt += 1
            # handles single or pairs of value bytes (i.e. low + high bytes)
            else:
                cmdList += [dictCmd[mycmd+cnt][0], "Val:{0:8}".format( \
                        sum_vals(vals[cnt:cnt+dictCmd[mycmd+cnt][1]])) ]
                cnt += dictCmd[mycmd+cnt][1]
    except KeyError:
        print "Bad packet?:", vals
        raise

    return cmdList
    
    
def translate_packet(byte_packet, id_dict, includetime=None):
    """Method returns structured human readable translation of bytes in a packet
    The goal of this method is not well quantified yet...
    
    Parameters
    ----------
    byte_packet : a list of integers
        Packets include 0xff 0xff and checksum. If a time stamp is present, the
        first entry in the list is a float.
    includetime : boolean, optional
        If true, packet time stamp (if one exists) will be converted to a string
        as well. If false, the packet time stamps are ignored.
    
    Returns
    -------
    retlist : list of strings
        If using a simple packet structure, generally of the form::
        
            [strID, strInst, strCmd1, strVal1, strCmd2, strVal2, [err], ...]

        Where an error string is included if checksum is invalid.
            
        Else if using sync-write packets, a list for each servo, and each list
        starts with a newline and tab::
        
            ['Sync-write',
            ['\n\t'+strID1, strCmd1, strVal1, strCmd2, strVal2, [err], ...],
            ['\n\t'+strID2, strCmd1, strVal1, strCmd2, strVal2, [err], ...],
            ....]
    """
    
    timestamp = []
    if byte_packet[0] != 255:
        if includetime:
            timestamp = ["Timestamp: {0:8}".format(byte_packet[0])]
        byte_packet = byte_packet[1:]
    
    if is_bad_packet(byte_packet):
        return ("bad packet; too short. expected: {0}; received: {1}".format( \
                _cmd, len(byte_packet)),)
    
    try:
        strInst = dictInstr[ byte_packet[_instr] ][0]
    except KeyError:
        return ("packet with bad instruction byte",)
        
    # Use information on lengths of commands to discern multiple
    #  commands, with commands potentially having varying numbers of value bytes
    #  e.g. setting goal position & moving speed, each with 2 value bytes
    mycmd = byte_packet[_cmd]

    checksum = 255 - (sum(byte_packet[2:-1]) % 256)
    if checksum == byte_packet[-1]:
        errstring = []#''
    else:
        errstring = ["invalid checksum {0:x} (actual {1:x})".format(
                byte_packet[-1], checksum)]
    # sync-write packet
    if byte_packet[_instr] == 0x83:
        retlist = ["Sync-write", ] + timestamp
        # iterate from first value byte, to byte before last byte (checksum),
        #  and iterate by length+1 bytes (ID + values) at a time
        subpackets = [ byte_packet[x:x+1+byte_packet[_synclen]] for x in
                range(_syncval, len(byte_packet)-1, 1+byte_packet[_synclen]) ]
                
        for subpacket in subpackets:
            # subpacketTranslated = vals_split_and_translate(subpacket,mycmd)
            subpacketTranslated = vals_split_and_translate(subpacket[1:],
                    mycmd, id_dict, subpacket[0])
            retlist.append( "\n\tID:{0:3}".format(subpacket[0]) )
            retlist += subpacketTranslated
            
        return retlist + errstring
    # read-data packet
    elif byte_packet[_instr] == 0x02:
        strID = "ID:{0:3}".format(byte_packet[_id])
        retlist = [strID, strInst]
        for cmd in xrange(byte_packet[_readcmd],
                byte_packet[_readcmd] + byte_packet[_readlen]):
            retlist.append( \
                    device_dict[id_dict[byte_packet[_id]]][cmd][0].strip() )
        return retlist + timestamp + errstring
    # write-data or reg-write packet
    else:
        strID = "ID:{0:3}".format(byte_packet[_id])
        strCmdsVals = vals_split_and_translate(byte_packet[_val:-1], mycmd,
                    id_dict, byte_packet[_id])
        
        return [strID, strInst] + strCmdsVals + timestamp + errstring
    
    
def main():
    """Parse command line options
    
    Points user to Readme.rst if script is called with no options.
    """
    
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    
    #
    parser.add_option('-i','--instructions',action="store_true", \
            dest="show_instr",default=False,help="Print list of instruction " \
            "bytes (e.g. read data). Default: %default")
    parser.add_option('-c','--commands',action="store_true", \
            dest="show_cmd",default=False,help="Print list of command " \
            "bytes (e.g. GOAL_POSITION). Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    if options.show_instr:
        show_instr()
        return
    if options.show_cmd:
        show_cmd()
        return
        
    print "PyDyPackets.py is a utility script, meant to be called by the " \
            "user. See 'Readme.rst' for a usage guide."
    return

    
if __name__ == '__main__':
    main()
