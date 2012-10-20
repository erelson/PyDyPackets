#! /usr/bin/env python

from optparse import OptionParser


# Global indices for getting bytes from packets;
# I'm doing this so I can easily toss the FF FF leading bytes if desired...
_id = 2
_len = 3    #note length is N + 2 where N is # of parameters
_instr = 4    # and N includes the Cmd value as well as the actual value bytes
_cmd = 5
_val = 6
_synclen = 6 #where the length of subpackets is specified for sync-write
_syncval = 7 #where the first subpacket begins for sync-writes

dictInstr = {0x01: ["ping      ", "0 "],
             0x02: ["read data ", "2 "],
             0x03: ["write data", "2~"],
             0x04: ["reg write ", "2~"],
             0x05: ["action    ", "0 "],
             0x06: ["reset     ", "0 "],
             0x83: ["sync write", "4~"]
            }
            
#          #cmd   # name                  #length of value
dictCmd = { 0  : ["MODEL_NUMBER_L        ",1],
            1  : ["MODEL_NUMBER_H        ",1],
            2  : ["VERSION               ",1],
            3  : ["SERVO_ID              ",1],
            4  : ["BAUD_RATE             ",1],
            5  : ["RETURN_DELAY_TIME     ",1],
            6  : ["CW_ANGLE_LIMIT_L      ",2],
            7  : ["CW_ANGLE_LIMIT_H      ",1],
            8  : ["CCW_ANGLE_LIMIT_L     ",2],
            9  : ["CCW_ANGLE_LIMIT_H     ",1],
            11 : ["LIMIT_TEMPERATURE     ",1],
            12 : ["LOW_LIMIT_VOLTAGE     ",1],
            13 : ["HIGH_LIMIT_VOLTAGE    ",1],
            14 : ["MAX_TORQUE_L          ",2],
            15 : ["MAX_TORQUE_H          ",1],
            16 : ["RETURN_LEVEL          ",1],
            17 : ["ALARM_LED             ",1],
            18 : ["ALARM_SHUTDOWN        ",1],
            20 : ["DOWN_CALIBRATION_L    ",2],
            21 : ["DOWN_CALIBRATION_H    ",1],
            22 : ["UP_CALIBRATION_L      ",2],
            23 : ["UP_CALIBRATION_H      ",1],
            24 : ["TORQUE_ENABLE         ",1],
            25 : ["LED                   ",1],
            26 : ["CW_COMPLIANCE_MARGIN  ",1],
            27 : ["CCW_COMPLIANCE_MARGIN ",1],
            28 : ["CW_COMPLIANCE_SLOPE   ",1],
            29 : ["CCW_COMPLIANCE_SLOPE  ",1],
            30 : ["GOAL_POSITION_L       ",2],
            31 : ["GOAL_POSITION_H       ",1],
            32 : ["GOAL_SPEED_L          ",2],
            33 : ["GOAL_SPEED_H          ",1],
            34 : ["TORQUE_LIMIT_L        ",2],
            35 : ["TORQUE_LIMIT_H        ",1],
            36 : ["PRESENT_POSITION_L    ",2],
            37 : ["PRESENT_POSITION_H    ",1],
            38 : ["PRESENT_SPEED_L       ",2],
            39 : ["PRESENT_SPEED_H       ",1],
            40 : ["PRESENT_LOAD_L        ",2],
            41 : ["PRESENT_LOAD_H        ",1],
            42 : ["PRESENT_VOLTAGE       ",1],
            43 : ["PRESENT_TEMPERATURE   ",1],
            44 : ["REGISTERED_INSTRUCTION",1],
            46 : ["MOVING                ",1],
            47 : ["LOCK                  ",1],
            48 : ["PUNCH_L               ",2],
            49 : ["PUNCH_H               ",1]
            }
    
    
def show_instr():
    """ """
    print ""
    print "In command line arguments (-i), enter the numeric value in column 3."
    print "\nInstruction:     Value:       # of parameters  "
    for key in dictInstr:
        print " {0:15}0x{1:<4X}{1:<4}{2:>12}".format(dictInstr[key][0],key,dictInstr[key][1])
        
    return
    
    
def show_cmd():
    """ """
    print ""
    print "In command line arguments (-c), enter the number value in column 2"
    print "\nCommand:                  Value:        valid range"
    for key in dictCmd:
        print "  {0:24}0x{1:<4X}{1:<4}{2:>8}".format(dictCmd[key][0],key,dictCmd[key][1])
    
    return
       

def sum_vals(byte_packet):
    """Sum value bytes by shifting the higher bytes as needed
    """
    val = 0
    # (byte_packet[_len] - 2 - 1) #length seems to be larger than it should be
    for i in xrange(byte_packet[_len] - 2 -1 ):
        val += byte_packet[_val+i]<<(8*i)
        
    return val
    
    
def sum_vals_2(bytes):
    """Sum value bytes by shifting the higher bytes as needed
    """
    val = 0
    # (byte_packet[_len] - 2 - 1) #length seems to be larger than it should be
    for i in xrange(len(bytes)):
        val += bytes[i]<<(8*i)
        
    return val
    
    
def vals_split_and_translate(vals, mycmd):
    """Return translated list of single or multiple commands
    
    Receives:
    vals - list of integers
    mycmd - integer of register to start writing bytes at
    """
    cnt = 0
    cmdList = list()
    while cnt < len(vals):
        # handle last byte in vals
        if cnt + 1 == len(vals):
            cmdList += [dictCmd[mycmd+cnt][0], "Val:{0:8}".format( \
                    sum_vals_2(vals[cnt:cnt+1]) ) ]
            cnt += 1
        else:
            cmdList += [dictCmd[mycmd+cnt][0], "Val:{0:8}".format( \
                       sum_vals_2(vals[cnt:cnt+dictCmd[mycmd+cnt][1]])) ]
            cnt += dictCmd[mycmd+cnt][1]
    return cmdList
    
    
def translate_packet(byte_packet):
    """Method returns partially human readable translations of bytes in a packet
    The goal of this method is not well quantified yet...
    
    Receives:
    byte_packet - a list of integers
    
    Returns:
    a list of strings;
            If using a simple packet structure, generally of the form:
                [strID, strInst, strCmd, strVal]
            Else if using sync-write packets:
                ....
    """
    
    if len(byte_packet) < _cmd: 
        return ("bad packet; too short. expected: {0}; received: {1}".format( \
                _cmd, len(byte_packet)),)
    
    strID = "ID:{0:3}".format(byte_packet[_id])
    try:
        strInst = dictInstr[ byte_packet[_instr] ][0]
    except KeyError:
        # print "packet with bad instruction byte"
        return ("packet with bad instruction byte",)
        
    # Use information on lengths of commands to discern multiple
    #  commands, with commands potentially having varying numbers of value bytes
    #  e.g. setting goal position & moving speed, each with 2 value bytes
    mycmd = byte_packet[_cmd]
    
    
    # cmdList = [mycmd, sum_vals_2( byte_packet[_val:_val+dictCmd[mycmd][1] ) ]
        

    
    if byte_packet[_instr] == 0x83:
        ret_list = ["Sync-write", ]
        # iterate from first value byte, to byte before last byte (checksum),
        #  and iterate by length+1 bytes (ID + values) at a time
        subpackets = [ byte_packet[x:x+1+byte_packet[_synclen]] for x in \
                range(_syncval, len(byte_packet)-1, 1+byte_packet[_synclen]) ]
                
        for subpacket in subpackets:
            # subpacketTranslated = vals_split_and_translate(subpacket,mycmd)
            subpacketTranslated = vals_split_and_translate(subpacket[1:],mycmd)
            ret_list.append( "\n\tID:{0:3}".format(subpacket[0]) )
            ret_list += subpacketTranslated
            
        return ret_list
            
    else:
        # strCmd = dictCmd[byte_packet[_cmd]][0]
        # val = sum_vals(byte_packet)
        # strVal = "Val:{0:8}".format(val)
        
        strCmdsVals = vals_split_and_translate(byte_packet[_val:], mycmd)
        
        return [strID, strInst] + strCmdsVals
    
    
def main():
    """Parse command line options
    
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
        
        
    return

    
if __name__ == '__main__':
    main()