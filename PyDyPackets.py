import httplib
import base64
import StringIO
import threading
import time
import wx
import logging  # prevents different threads' output from mixing

import serial

if __name__ == '__main__':
    
    
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
                
                
    # xBee serial port settings
    myPort = 16 #15 #~ note: use port number - 1
    # myPort = 16 #15 #~ note: use port number - 1
    myBaud = 1000000
    
    def COMThread(byte_packet):
        """
        Receives:
        byte_packet - a BytePacket
        """
        byte_string = ""
        logging.debug( 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        byte_list = list()
        byte_packet.word = list()
        while True:
        
            # If xbee serial port was opened and is open.
            if serExist and ser.isOpen():
                # read all bytes in the buffer
                byte = None
                while ser.inWaiting():
                    
                    # print '...'
                    
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
                        byte_packet.word = [0xff,0xff] + byte_list[:-2]
                        logging.debug(("packet:", byte_packet.word, \
                            byte_list[-3:-2] == [255 - (sum(byte_list[:-3]) % 256)] ))
                        byte_list = list()
                        
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
        print "Successfully connected to port {0} at {1} baud".format(myPort,myBaud)
        serExist = 1
    
    except serial.SerialException:
        print "Couldn't open xBee serial port. Try again later."
        serExist = 0
    
    
    myoldbytelist = None
    mybyte_list = BytePacket()
    
    thread = threading.Thread(target=COMThread, args=(mybyte_list,))
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
    
    
