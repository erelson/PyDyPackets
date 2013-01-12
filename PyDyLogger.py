#! /usr/bin/env python

from PyDyConfig import port, baud, timing
from PyDyPackets import translate_packet

import threading
# import time
import logging  # prevents different threads' output from mixing
import serial
import time
from optparse import OptionParser


######################################
# Serial port settings are managed in your 'Config/pydypackets.cfg' file.

def logger_method(translate=False, saveall=False, outputfile="logging_output.txt"):
    """Method opens serial port and stores received byte packets.
    
    Parameters
    ----------
    saveall : boolean
        Controls whether malformed packets are saved
    translate : boolean
        If true, packets are displayed in human readable form
    """
    
    logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)
                    
    if timing: startTime = time.time()
                        
    class BytePacket(object):
        """Class for passing byte packet between threads
        
        Includes a Lock object, but this has not been used or found necessary.
        """
        
        def __init__(self, start=0):
            self.lock = threading.Lock()
            self.word = []
            self.timestamp = 0.0
                
    
    def COMThread(byte_packet, saveall=False, translate=False):
        """Method monitors serial port and sends packets to output
        
        Method is intended to be run in a threading.thread.
        
        Receives
        ----------
        byte_packet : BytePacket object
            A BytePacket object allowing external thread access to the current 
            packet
        saveall : boolean
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
                    # We use FF FF to identify *end* of packet.
                    if byte_list[-2:] == [0xff,0xff]:
                        
                        checksumOK = byte_list[-3] == \
                                255 - (sum(byte_list[:-3]) % 256)
                        
                        # Save packet
                        # Note: saved packets have FF FF prepended to them
                        if saveall:
                            byte_packet.word = [0xff,0xff] + byte_list[:-2]
                        elif checksumOK:
                            byte_packet.word = [0xff,0xff] + byte_list[:-2]
                        else:
                            continue
                        
                        if translate:
                            # logging.debug("\t".join(translate_packet(byte_packet.word)))
                            print "\t".join(translate_packet(byte_packet.word))
                        else:
                            logging.debug(("packet: " + \
                                    " ".join(["{0:<3}".format(x) \
                                    for x in byte_packet.word]) + \
                                    "  packet ok?: " + str(checksumOK )))
                                    
                        # Get packet time
                        if timing:
                            byte_packet.timestamp = time.time() - startTime
                        
                        byte_list = list()
                        
                    # Threshold to keep byte_list at a reasonable size.
                    # 108 chosen as 4 + 4 + 20 * 5, e.g. sending speed/position
                    #  to 20 servos...
                    if len(byte_list) > 108: 
                        byte_list = list()
    
    
    # Main thread:
    
    # Opening the serial port
    try:
        ser = serial.Serial(port, baud)
        print "Successfully connected to port {0} at {1} baud".format( \
                port, baud)
        serExist = 1
    
    except serial.SerialException as e:
        print "Couldn't open serial port {0}. Try again later.".format(port)
        print e
        serExist = 0
    
    
    mybyte_packet = BytePacket()
    
    # Create serial port monitoring thread
    thread = threading.Thread(target=COMThread, args=(mybyte_packet,), \
            kwargs={'translate': translate, 'saveall': saveall})
    # thread = threading.Thread(target=COMThread, args=(mybyte_packet,))
    # thread = threading.Thread(target=COMThread, kwargs={'byte_packet': mybyte_packet})
    thread.daemon = True # Thread is killed when main thread ends.
    thread.start()
    
    with open(outputfile,'w') as fw:
        try:
            if timing: # use timing to differentiate new packets
                myoldtimestamp = 0.0
                while True:
                    if mybyte_packet.timestamp != myoldtimestamp:
                        myoldtimestamp = mybyte_packet.timestamp
                        
                        # Record packet timestamp
                        if timing:
                            fw.write("{0:.3f} ".format(mybyte_packet.timestamp) + " ")
                        
                        fw.write(" ".join([str(x) for x in mybyte_packet.word]) + "\n")
                    
            else: # packets are differentiated by their contents
                myoldbytelist = None
                while True:
                    if mybyte_packet.word != myoldbytelist:
                        myoldbytelist = mybyte_packet.word
                        
                        fw.write(" ".join([str(x) for x in mybyte_packet.word]) + "\n")
                    
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
            dest="saveall",default=False,help="Optionally save all bytes/" \
            "packets, including malformed packets. Default: %default")
    parser.add_option('-o','--output',action="store", \
            dest="output",default="logging_output.txt",help="Specify output " \
            "file for log of packets. Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    logger_method(translate=options.translate, saveall=options.saveall, \
            outputfile=options.output)
    
    return

    
if __name__ == '__main__':
    main()
