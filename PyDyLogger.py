#! /usr/bin/env python

import PyDyConfig

import threading
# import time
import logging  # prevents different threads' output from mixing

from PyDyPackets import translate_packet

import serial
from optparse import OptionParser


######################################
# Serial port settings #

# Linux: Two ways to specify##############
#myPort = 16
#myPort = '/dev/ttyS1'
#myPort = '/dev/ttyACM0'

# Windows: Two ways to specify ############
myPort = "COM17" # string specification works for windows
#myPort = 16 # == COM17 for Windows #~ Note on Windows: use port number - 1 on windows OR:

# Baud rate of Dynamixel bus
myBaud = 1000000
######################################


def logger_method(translate=False, save_all=False):
    """Method opens serial port and stores received byte packets.
    
    Receives:
    save_all - Controls whether malformed packets are saved
    translate - If true, packets are displayed in human readable form
    """
    
    logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)
                        
    class BytePacket(object):
        """Class for passing byte packet between threads
        
        Includes a Lock object, but this has not been used or found necessary.
        """
        
        def __init__(self, start=0):
            self.lock = threading.Lock()
            self.word = []
                
    
    def COMThread(byte_packet, save_all=False, translate=False):
        """Method monitors serial port and sends packets to output
        
        Method is intended to be run in a threading.thread.
        
        Receives
        ----------
        byte_packet : BytePacket object
            a BytePacket object allowing external access to the
            current packet
        save_all : boolean
            Controls whether malformed packets are saved
        translate : boolean
            If true, packets are displayed in human readable form
        """
        
        byte_list = list()
        byte_packet.word = list()
        
        while True:
        
            # If serial port was opened and is open.
            if serExist and ser.isOpen():
                # read all bytes in the buffer
                byte = None
                while ser.inWaiting():
                    # Read bytes and add them to byte_list
                    byte = ser.read()
                    if byte != None and byte !="": 
                        try:
                            byte_list.append(int(byte.encode('hex'),16))
                            
                        except ValueError as e:
                            logging.debug(( 'error', byte, e,))
                    
                    # Identify and vet packets; 
                    # We use FF FF to indicate *end* of packet...
                    if byte_list[-2:] == [0xff,0xff]:
                        
                        checksumOK = byte_list[-3] == \
                                255 - (sum(byte_list[:-3]) % 256)
                        
                        # Note: saved packets have FF FF prepended to them
                        if save_all:
                            byte_packet.word = [0xff,0xff] + byte_list[:-2]
                        elif checksumOK:
                            byte_packet.word = [0xff,0xff] + byte_list[:-2]
                        
                        if translate:
                            # logging.debug("\t".join(translate_packet(byte_packet.word)))
                            print "\t".join(translate_packet(byte_packet.word))
                        else:
                            logging.debug(("packet: " + \
                                    " ".join(["{0:<3}".format(x) \
                                    for x in byte_packet.word]) + \
                                    "  packet ok?: " + str(checksumOK )))
                                
                        byte_list = list()
                        
                    # threshold to keep byte_list at a reasonable size.
                    # 108 chosen as 4 + 4 + 20 * 5, e.g. sending speed/position
                    #  to 20 servos...
                    if len(byte_list) > 108: 
                        byte_list = list()
    
    # Opening the serial port
    try:
        ser = serial.Serial(myPort, myBaud)
        print "Successfully connected to port {0} at {1} baud".format( \
                myPort,myBaud)
        serExist = 1
    
    except serial.SerialException:
        print "Couldn't open serial port {0}. Try again later.".format(myPort)
        serExist = 0
    
    
    myoldbytelist = None
    mybyte_list = BytePacket()
    
    thread = threading.Thread(target=COMThread, args=(mybyte_list,), \
            kwargs={'translate': translate, 'save_all': save_all})
    # thread = threading.Thread(target=COMThread, args=(mybyte_list,))
    # thread = threading.Thread(target=COMThread, kwargs={'byte_packet': mybyte_list})
    thread.daemon = True # Thread is killed when main thread ends.
    thread.start()
    
    outputfile="default_out"
    with open(outputfile,'w') as fw:
        try:
            while True:
                if mybyte_list.word != myoldbytelist:
                    myoldbytelist = mybyte_list.word
                    
                    fw.write(" ".join([str(x) for x in myoldbytelist]) + "\n")
                    
        except KeyboardInterrupt:
            print "KeyboardInterrupt caught! Closing {0}...".format(outputfile)
    
    return
    
    
def main():
    """Parse command line options
    
    """
    
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    
    #
    parser.add_option('-t','--translate',action="store_true", \
            dest="translate",default=False,help="Print human readable " \
            "packets. Default: %default")
    parser.add_option('-a','--all',action="store_true", \
            dest="save_all",default=False,help="Optionally save all bytes/" \
            "packets, including malformed packets. Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    logger_method(translate=options.translate, save_all=options.save_all)
    
    
    return

    
if __name__ == '__main__':
    main()
