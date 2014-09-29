""" Module PyDyParser currently handles filtering and tallying packets

"""

from pydypackets.PyDyPackets import _id, _cmd, _instr, _len, _synclen, _syncval, \
                        is_bad_packet


def filtering_method(stream, f_id=None, f_instr=None, f_cmd=None, \
            sync_split=False):
    """Returns a filtered list of byte packets from a file stream

    Filtering includes the ability to automatically split
    sync-write packets into their per-servo commands.

    Parameters
    ----------
    stream : a file stream, e.g. via open('file', 'r')
    (**optional**)
    f_id : list/tuple of integers
        ID #s to keep
    f_instr : list/tuple of integers
        Instruction values to keep
    f_cmd : list/tuple of integers
        Command values (start addresses) to keep
    sync_split : boolean
        If true, convert sync-write packets into artificial individual packets.
        Packet time-stamp of the sync-write packet is applied to each
        sub-packet.

    Returns
    -------
    filtered : list of lists of integers
        A list of filtered packets; each packet is a list of integers
    """
    
    f_id = _is_list(f_id)
    f_instr = _is_list(f_instr)
    f_cmd = _is_list(f_cmd)
    
    # split up sync packets if enabled, and not filtering for sync packets
    if sync_split and (len(f_instr) and 0x83 not in f_instr):
        f_instr.append(0x83)
    
    filtered = list()
    for line in stream:
        packet = line.split()
        if packet == []: continue
        
        # Look for integer and or hex ("\xFF") strings instead of a timestamp
        if packet[0] != "255" and packet[0].decode('string-escape') != "\xff" \
                and packet[0].lower() != "0xff":
            try:
                time = [float(packet[0])]
            except ValueError:
                print "Possibly helpful debug info:"
                print "repr(packet[0]):", repr(packet[0])
                print "len(packet[0]):", len(packet[0])
                print "packet[0].decode('string-escape'):", \
                        packet[0].decode('string-escape')
                print "len(packet[0].decode('string-escape')):", \
                        len(packet[0].decode('string-escape'))
                raise
            packet = packet[1:]
        else: time = []

        if packet[0].decode('string-escape') == '\xff': # Note: \xff is a single byte: len('\xff')==1
            packet = [ord(_.decode('string-escape')) for _ in  packet]
        else: # handle 255 or 0xFF styles
            packet = [int(_, 0) for _ in packet]
        
        if is_bad_packet(packet):
            continue
        
        # check packet contents against the filters
        if (f_id == None or packet[_id] in f_id or sync_split) and \
                (f_cmd == None or packet[_cmd] in f_cmd) and \
                (f_instr == None or packet[_instr] in f_instr):
            # split up sync-write packets
            if sync_split and packet[_instr] == 0x83 and \
                    (f_instr == None or 0x03 in f_instr):
                for subpacket in make_packets_from_sync_write_packet(packet):
                    if (f_id == None or subpacket[_id] in f_id):
                        filtered.append(time + subpacket)
            else:
                filtered.append(time + packet)
    
    return filtered

    
def make_packets_from_sync_write_packet(packet):
    """Method receives a stream of sync-write bytes, with the length of each
    subpacket
    
    Parameters
    ----------
    packet : list of integers
        List of bytes in a packet, including FF FF.
        Do not include timestamp.
        
    Returns
    -------
    packet_list : list of lists of integers
        Byte packets
        
    Notes
    ------
    Sync write packets are...
    
    See Also
    --------
    Pgs. 19 & 23 of AX-12 manual.

    """
    sublength = packet[_synclen]
    numsubpackets = (packet[_len] - 4) / (sublength + 1)
    command = packet[_cmd]
    packet_list = []
    # Sync packet format:
    # FF FF FE length 83 cmd sublength ID1 vals[1,sublen] ID2 vals ... checksum
    subpackets = [ packet[x:x + sublength + 1] \
            for x in range(_syncval, packet[_len] + 4 - 1, sublength + 1) ]
                
    # Build new packets
    for subpacket in subpackets:
        # FF FF ID sublength+3 03 cmd vals[1,sublength] checksum
        newpacket = [0xFF, 0xFF, subpacket[0], sublength+3, 0x03, command] + \
                subpacket[1:]
        checksum = 255 - (sum(newpacket[2:]) % 256)
        packet_list.append(newpacket + [checksum])
        
    return packet_list


def tally_packets(packet_list, tally_by='cmd', **kwargs):
    """Method reports the # of packets of each type
    
    Type depends on the value passed to the tally_by argument
    
    Parameters
    ----------
    packet_list : list of lists of integers
        A list of packets; each packet is a list of integers.
        Alternately, packet_list will be read from a file if the file kwarg is
        passed.
    tally_by : string
        Which byte to tally packets by.
        Valid values for tally_by are 'cmd', 'instr', 'id', 'len'.
    kwargs : optional
        file : string
            file of packets to read in
    """
    
    dict_tally_by = {     'cmd'   : _cmd,
                          'instr' : _instr,
                          'id'    : _id,
                          'len'   : _len
                          }
    
    if tally_by not in dict_tally_by:
        return 0
    
    # read file into packet_list if 'file' kwarg was given
    if 'file' in kwargs:
        packet_list = list()
        with open(kwargs['file'], 'r') as fr:
            for line in fr:
                packet_list.append( [int(x, 0) for x  in line.split()] )
    # else if packet_list is already a list of packets...
    elif packet_list != None:
        pass
    # I think I forgot a logic case here??
    else:
        return 0
        
    # Do the tallying
    
    # First create list of the nth byte from each packet
    # try:
    tally_list = [packet[dict_tally_by[tally_by]] for \
            packet in packet_list if packet != [] ]
    tallied_list = tally(tally_list)
    print "Tally results:"
    print "Val:   Instances:"
    for entry in tallied_list:
        print " {0:<7}{1}".format(entry[0],entry[1])
    # catch case where ... ?
    # except:
        # return 2
    
    return tallied_list
    
    
def _is_list(f_thing):
    """Try various ways to assure that we have a filter list.
    This is just for the heck of it... excessive flexibility...
    
    Parameters
    ----------
    f_thing : string or list
        Represents list of numeric filters (e.g. servo ID, instruction byte)
    
    Returns
    -------
    f_thing : list
        Returns list unless invalid input, in which case None is returned.
    """
    
    if f_thing == None:
        return None
    
    try:
        f_thing = f_thing.split(',')
        f_thing = [int(x) for x in f_thing]
    except AttributeError:
        pass # is probably a list already
    except ValueError:
        print "Non-numeric filter(s) given: {0}".format(f_thing)
        f_thing = None
    # except: # may have forgotten an easy-to-get exception
        
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
    
    Parameters
    ----------
    list : list of anything
    
    Returns
    -------
    tally list : list of tuples
        Each tuple is of the form (item, # occurences of item)
    """
    
    uniqueSet = []
    for item in list:
        if item not in uniqueSet:
            uniqueSet.append(item)
    return [(item, list.count(item)) for item in uniqueSet]
