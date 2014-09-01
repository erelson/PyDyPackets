from pydypackets import PyDyPackets
from pydypackets.PyDyConfig import PyDyConfigParser


cfg = PyDyConfigParser()
cfg.read()
port, baud, __, timing, __ = cfg.get_params()
id_dict = cfg.get_id_to_device_dict()

def test_vals_split_and_translate_runs():
    # Ping packet for servo id 0C.
    testpacket = [0xff, 0xff, 0x0c, 0x02, 0x01, 0xec]
    PyDyPackets.vals_split_and_translate(testpacket, 2, id_dict)

def test_vals_split_and_translate_keyerr():
    # should fail due to lack of a servo with ID FC.
    testpacket = [0xff, 0xff, 0xfc, 0x02, 0x01, 0xec]
    PyDyPackets.vals_split_and_translate(testpacket, 2, id_dict)
