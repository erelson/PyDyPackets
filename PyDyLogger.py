#! /usr/bin/env python
import base64
import StringIO
import threading
import time
import logging  # prevents different threads' output from mixing

import PyDyPackets

import serial
from optparse import OptionParser

def logger_method(translate=False):
    """ """
    
                
    # Serial port settings
    myPort = 16 #=17 #~ note: use port number - 1
    myBaud = 1000000
    
    
    logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)
                        
    class BytePacket(object):
        def __init__(self, start=0):
            self.lock = threading.Lock()
            self.word = []
            
        def increment(self):
            # logging.debug('Waiting for lock; {0}'.format(self.value))
            print self.lock.acquire()
                
            try:
                # logging.debug('Acquired lock')
                self.value = self.value + 1
            finally:
                self.lock.release()
                
    
    def COMThread(byte_packet, saveAll=False, translate=False):
        """
        Receives:
        byte_packet - a BytePacket
        """
        
        byte_string = ""
        byte_list = list()
        byte_packet.word = list()
        
        while True:
        
            # If xbee serial port was opened and is open.
            if serExist and ser.isOpen():
                # read all bytes in the buffer
                byte = None
                while ser.inWaiting():
                    
                    byte = ser.read()
                    
                    if byte != None and byte !="": 
                        try:
                            byte_list.append(int(byte.encode('hex'),16))
                            # print int(byte.encode('hex'),16), byte_list[-2:]
                        except ValueError as e:
                            logging.debug(( 'error', byte, e,))
                    
                    if byte_list[-2:] == [0xff,0xff]:
                        # print "packet:", [0xff,0xff], byte_list[:-2]
                        # print "old:", byte_packet.word
                        
                        checksumOK = byte_list[-3:-2] == [255 - (sum(byte_list[:-3]) % 256)]
                        
                        if saveAll:
                            byte_packet.word = [0xff,0xff] + byte_list[:-2]
                        elif checksumOK:
                            byte_packet.word = [0xff,0xff] + byte_list[:-2]
                        
                        if translate:
                            # logging.debug("\t".join(PyDyPackets.translate_packet(byte_packet.word)))
                            print "\t".join(PyDyPackets.translate_packet(byte_packet.word))
                        else:
                            logging.debug(("packet:", byte_packet.word, "packet ok?:", \
                                checksumOK ))
                                
                        byte_list = list()
                        
                    # arbitrary threshold to keep byte_list at a reasonable size.
                    if len(byte_list) > 12:
                        byte_list = list()
                    # byte_string = byte_string + byte
                    # byte_list.append(int(byte.encode('hex'),16))
                    # if the end of packet symbol is seen...
                    # if byte == ')':
                    # if byte_string[:-2] == str(0xFF)+str(0xFF)):
                    
                # if byte != None and byte !="": 
                    # try:
                        # print int(byte.encode('hex'),16)
                    # except ValueError as e:
                        # print 'error', byte, e

    
    # Opening the serial port
    try:
        ser = serial.Serial(myPort,myBaud) #port number - 1
        print "Successfully connected to port {0} at {1} baud".format(myPort+1,myBaud)
        serExist = 1
    
    except serial.SerialException:
        print "Couldn't open serial port {0}. Try again later.".format(myPort+1)
        serExist = 0
    
    
    myoldbytelist = None
    mybyte_list = BytePacket()
    
    thread = threading.Thread(target=COMThread, args=(mybyte_list,),kwargs={'translate': translate})
    # thread = threading.Thread(target=COMThread, args=(mybyte_list,))
    # thread = threading.Thread(target=COMThread, kwargs={'byte_packet': mybyte_list})
    thread.daemon = True
    thread.start()
    
    outputfile="default_out"
    with open(outputfile,'w') as fw:
        try:
            while True:
                if mybyte_list.word != myoldbytelist:
                    myoldbytelist = mybyte_list.word
                    # logging.debug(("bahhaah", myoldbytelist,))
                    # logging.debug("")
                    fw.write(" ".join([str(x) for x in myoldbytelist]))
                    fw.write("\n")
                    
        except KeyboardInterrupt:
            print "KeyboardInterrupt caught! Closing {0}...".format(outputfile)
    
    # app.MainLoop()
    
    
def main():
    """Parse command line options
    
    """
    
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    
    #
    parser.add_option('-t','--translate',action="store_true", \
            dest="translate",default=False,help="Print human readable " \
            "packets. Default: %default")
    #
    
    (options, args) = parser.parse_args()
    
    logger_method(translate=options.translate)
        
    
    return
    
if __name__ == '__main__':
    main()
