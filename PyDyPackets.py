#! /usr/bin/env python
from optparse import OptionParser
import base64
import StringIO

# Global indices for getting bytes from packets;
# I'm doing this so I can easily toss the FF FF leading bytes if desired...
_id = 2
_len = 3    #note length is N + 2 where N is # of parameters
_instr = 4    # and N includes the Cmd value as well as the actual value bytes
_cmd = 5
_val = 6



dictInstr = {0x01: "ping      ",
             0x02: "read data ",
             0x03: "write data",
             0x04: "reg write ",
             0x05: "action    ",
             0x06: "reset     ",
             0x83: "sync write"}
             
dictCmd = { 0  : "MODEL_NUMBER_L       ",
            1  : "MODEL_NUMBER_H       ",
            2  : "VERSION              ",
            3  : "SERVO_ID             ",
            4  : "BAUD_RATE            ",
            5  : "RETURN_DELAY_TIME    ",
            6  : "CW_ANGLE_LIMIT_L     ",
            7  : "CW_ANGLE_LIMIT_H     ",
            8  : "CCW_ANGLE_LIMIT_L    ",
            9  : "CCW_ANGLE_LIMIT_H    ",
            11 : "LIMIT_TEMPERATURE    ",
            12 : "LOW_LIMIT_VOLTAGE    ",
            13 : "HIGH_LIMIT_VOLTAGE   ",
            14 : "MAX_TORQUE_L         ",
            15 : "MAX_TORQUE_H         ",
            16 : "RETURN_LEVEL         ",
            17 : "ALARM_LED            ",
            18 : "ALARM_SHUTDOWN       ",
            20 : "DOWN_CALIBRATION_L   ",
            21 : "DOWN_CALIBRATION_H   ",
            22 : "UP_CALIBRATION_L     ",
            23 : "UP_CALIBRATION_H     ",
            24 : "TORQUE_ENABLE        ",
            25 : "LED                  ",
            26 : "CW_COMPLIANCE_MARGIN ",
            27 : "CCW_COMPLIANCE_MARGIN",
            28 : "CW_COMPLIANCE_SLOPE  ",
            29 : "CCW_COMPLIANCE_SLOPE ",
            30 : "GOAL_POSITION_L      ",
            31 : "GOAL_POSITION_H      ",
            32 : "GOAL_SPEED_L         ",
            33 : "GOAL_SPEED_H         ",
            34 : "TORQUE_LIMIT_L       ",
            35 : "TORQUE_LIMIT_H       ",
            36 : "PRESENT_POSITION_L   ",
            37 : "PRESENT_POSITION_H   ",
            38 : "PRESENT_SPEED_L      ",
            39 : "PRESENT_SPEED_H      ",
            40 : "PRESENT_LOAD_L       ",
            41 : "PRESENT_LOAD_H       ",
            42 : "PRESENT_VOLTAGE      ",
            43 : "PRESENT_TEMPERATURE  ",
            44 : "REGISTERED_INSTRUCTIO",
            46 : "MOVING               ",
            47 : "LOCK                 ",
            48 : "PUNCH_L              ",
            49 : "PUNCH_H              "
            }
    
def show_instr():
    """ """
    print "\nIn command line arguments, enter the numeric value in column 3."
    print "\nInstruction:     Value:       # of parameters  "
    print " ping           0x01  1             0        "
    print " read data      0x02  2             2        "
    print " write data     0x03  3             2~       "
    print " reg write      0x04  4             2~       "
    print " action         0x05  5             0        "
    print " reset          0x06  6             0        "
    print " sync write     0x83  131           4~       "
    
    return
    
def translate_packet(byte_list):
    """ 
    Receives:
    byte_list - a list of integers
    """
    
    if len(byte_list) < _cmd: 
        return ("bad packet; too short.",)
    
    strID = "ID:{0:3}".format(byte_list[_id])
    try:
        strInst = dictInstr[ byte_list[_instr] ]
    except KeyError:
        # print "packet with bad instruction byte"
        return ("packet with bad instruction byte",)
    
    strCmd = dictCmd[byte_list[_cmd]]
    
    val = 0
    # (byte_list[_len] - 2 - 1) #length seems to be larger than it should be
    for i in xrange(byte_list[_len] - 2 -1 ):
        val += byte_list[_val+i]<<(8*i)
        
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
            "bytes. Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    if options.show_instr:
        show_instr()
        return
        
    
    return

if __name__ == '__main__':
    main()