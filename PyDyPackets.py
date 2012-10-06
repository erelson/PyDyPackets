#! /usr/bin/env python
from optparse import OptionParser


# Global indices for getting bytes from packets;
# I'm doing this so I can easily toss the FF FF leading bytes if desired...
_id = 2
_len = 3    #note length is N + 2 where N is # of parameters
_instr = 4    # and N includes the Cmd value as well as the actual value bytes
_cmd = 5
_val = 6

dictInstr = {0x01: ["ping      ", "0 "],
             0x02: ["read data ", "2 "],
             0x03: ["write data", "2~"],
             0x04: ["reg write ", "2~"],
             0x05: ["action    ", "0 "],
             0x06: ["reset     ", "0 "],
             0x83: ["sync write", "4~"]
            }
             
dictCmd = { 0  : ["MODEL_NUMBER_L        ","?"],
            1  : ["MODEL_NUMBER_H        ","?"],
            2  : ["VERSION               ","?"],
            3  : ["SERVO_ID              ","?"],
            4  : ["BAUD_RATE             ","?"],
            5  : ["RETURN_DELAY_TIME     ","?"],
            6  : ["CW_ANGLE_LIMIT_L      ","?"],
            7  : ["CW_ANGLE_LIMIT_H      ","?"],
            8  : ["CCW_ANGLE_LIMIT_L     ","?"],
            9  : ["CCW_ANGLE_LIMIT_H     ","?"],
            11 : ["LIMIT_TEMPERATURE     ","?"],
            12 : ["LOW_LIMIT_VOLTAGE     ","?"],
            13 : ["HIGH_LIMIT_VOLTAGE    ","?"],
            14 : ["MAX_TORQUE_L          ","?"],
            15 : ["MAX_TORQUE_H          ","?"],
            16 : ["RETURN_LEVEL          ","?"],
            17 : ["ALARM_LED             ","?"],
            18 : ["ALARM_SHUTDOWN        ","?"],
            20 : ["DOWN_CALIBRATION_L    ","?"],
            21 : ["DOWN_CALIBRATION_H    ","?"],
            22 : ["UP_CALIBRATION_L      ","?"],
            23 : ["UP_CALIBRATION_H      ","?"],
            24 : ["TORQUE_ENABLE         ","?"],
            25 : ["LED                   ","?"],
            26 : ["CW_COMPLIANCE_MARGIN  ","?"],
            27 : ["CCW_COMPLIANCE_MARGIN ","?"],
            28 : ["CW_COMPLIANCE_SLOPE   ","?"],
            29 : ["CCW_COMPLIANCE_SLOPE  ","?"],
            30 : ["GOAL_POSITION_L       ","?"],
            31 : ["GOAL_POSITION_H       ","?"],
            32 : ["GOAL_SPEED_L          ","?"],
            33 : ["GOAL_SPEED_H          ","?"],
            34 : ["TORQUE_LIMIT_L        ","?"],
            35 : ["TORQUE_LIMIT_H        ","?"],
            36 : ["PRESENT_POSITION_L    ","?"],
            37 : ["PRESENT_POSITION_H    ","?"],
            38 : ["PRESENT_SPEED_L       ","?"],
            39 : ["PRESENT_SPEED_H       ","?"],
            40 : ["PRESENT_LOAD_L        ","?"],
            41 : ["PRESENT_LOAD_H        ","?"],
            42 : ["PRESENT_VOLTAGE       ","?"],
            43 : ["PRESENT_TEMPERATURE   ","?"],
            44 : ["REGISTERED_INSTRUCTION","?"],
            46 : ["MOVING                ","?"],
            47 : ["LOCK                  ","?"],
            48 : ["PUNCH_L               ","?"],
            49 : ["PUNCH_H               ","?"]
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
    
    
def translate_packet(byte_packet):
    """ 
    Receives:
    byte_packet - a list of integers
    """
    
    if len(byte_packet) < _cmd: 
        return ("bad packet; too short.",)
    
    strID = "ID:{0:3}".format(byte_packet[_id])
    try:
        strInst = dictInstr[ byte_packet[_instr] ][0]
    except KeyError:
        # print "packet with bad instruction byte"
        return ("packet with bad instruction byte",)
    
    strCmd = dictCmd[byte_packet[_cmd]][0]
    
    val = sum_vals(byte_packet)
        
    strVal = "Val:{0:8}".format(val)
    
    return (strID, strInst, strCmd, strVal)
    
    
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
    parser.add_option('-t','--test',action="store", \
            dest="listtest",default=None,help="Print list of command " \
            "bytes (e.g. GOAL_POSITION). Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    print options.listtest
    
    if options.show_instr:
        show_instr()
        return
    if options.show_cmd:
        show_cmd()
        return
        
        
    return

    
if __name__ == '__main__':
    main()