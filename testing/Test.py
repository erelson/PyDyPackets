# This should be invoked from the top level of the package directory as "python testing/Test.py"
# Currently a bunch of the checksums are wrong.
# In lieu of doing actual testing, this [was] is my current test-suite. I'm a bad man.
    
from pydypackets import PyDyPackets as PDP
from pydypackets import PyDyParser as PDPar
from pydypackets.PyDyConfig import PyDyConfigParser


cfg = PyDyConfigParser()
cfg.read()
port, baud, __, timing, __ = cfg.get_params()
z = cfg.get_id_to_device_dict() # z = id_dict

print '\t'.join(PDP.translate_packet([ \
        0XFF,0XFF,0XFE,0X18,0X83,0X1E,0X04,0X00,0X10,0X00,0X50,
        0X01,0X01,0X20,0X02,0X60,0X03,0X02,0X30,0X00,0X70,0X01,
        0X03,0X20,0X02,0X80,0X03,0X12], z) )
print "non-sync-write tests:"
print '\t'.join(PDP.translate_packet([0xff,0xff,0x00,0x02,0x00,0xfd], z))

print '\t'.join(PDP.translate_packet([255,255,52,5,3,8,255,3,185], z)) #write
print '\t'.join(PDP.translate_packet([255,255,61,5,3,30,235,1,176], z)) #write
print '\t'.join(PDP.translate_packet([0xff,0xff,0x00,0x04,0x03,0x04,0x01,0xf3], z)) # write
print '\t'.join(PDP.translate_packet([0xff,0xff,0x00,0x03,0x03,0x04,0xf2], z)) # write
print '\t'.join(PDP.translate_packet([0xff,0xff,0x01,0x04,0x02,0x00,0x03,0xf5], z)) #read data
print '\t'.join(PDP.translate_packet([0xff,0xff,0x00,0x02,0x06,0xf7], z)) #reset
print '\t'.join(PDP.translate_packet([0xff,0xff,0x01,0x02,0x01,0xfb], z)) #ping
print '\t'.join(PDP.translate_packet([0xff,0xff,0x01,0x02,0x05,0xf7], z)) #action
print '\t'.join(PDP.translate_packet([0xff,0xff,0x00,0x07,0x03,0x1e,0x00,0x02,0x00,0x02,0xd3], z)) #example 18

print "\nWith timestamps..."
print "\t".join(PDP.translate_packet([123.445,0xff,0xff,0x00,0x04,0x03,0x04,0x01,0xf3], z, True)) # write
print '\t'.join(PDP.translate_packet([123.445, \
        0XFF,0XFF,0XFE,0X18,0X83,0X1E,0X04,
        0X00,0X10,0X00,0X50,0X01,
        0X01,0X20,0X02,0X60,0X03,
        0X02,0X30,0X00,0X70,0X01,
        0X03,0X20,0X02,0X80,0X03,
        0X12], z, True) )
print "\nSplit sync packet"
mypackets = PDPar.make_packets_from_sync_write_packet([ \
        0XFF,0XFF,0XFE,0X18,0X83,0X1E,0X04,
        0X00,0X10,0X00,0X50,0X01,
        0X01,0X20,0X02,0X60,0X03,
        0X02,0X30,0X00,0X70,0X01,
        0X03,0X20,0X02,0X80,0X03,
        0X12])

for x in mypackets:
    print x
    print "\t".join(PDP.translate_packet(x, z, True))
