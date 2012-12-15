###WORK IN PROGRESS

import ConfigParser
from sys import exit

config = ConfigParser.ConfigParser()

#######################################
# Either pydypackets.cfg or pydypackets.txt are valid config files.
status = config.read("Config/pydypackets.cfg")
if status == []:
    status = config.read("Config/pydypackets.txt")
if status == []:
    print "\nERROR: no config file exists. Create a pydypackets.cfg file in " \
            "the Config/ folder. See Config/config_example.cfg for more info."
    print "\nFor PyDyPackets usage guide, and more info, see 'Readme.rst'."
    exit()
    

#######################################
# Read in other bot profile(s) (overwrite the initial configs that both
#  files define;)
if config.has_section("bots"):
    for profile in config.items("bots"):
        config.read(profile[1]) # UNTESTED

#######################################
# Create device ID to device type dictionary
if config.has_section("id_to_device_type"):
    id_dict = dict([ (int(x[0]), x[1]) for x in \
            config.items("id_to_device_type")])
else:
    id_dict = dict([ ("default_device_type", "AX-12") ])

#######################################
# Create device ID to device type dictionary
if config.has_section("limits"):
    #id_dict = dict([ (int(x[0]), x[1]) for x in \
    #        config.items("id_to_device_type")])
    pass
else:
    pass
    #id_dict = dict([ ("default_device_type", "AX-12") ])

#######################################
# Get plotting layout information
if config.has_section("plotting"):
    dict_subplot = dict([ (int(x[0]), int(x[1])) for x in \
            config.items("plotting")])
    
#######################################
# Grab single value parameters

# This list stores 
#  (1) section containing parameter in pydypackets.cfg
#  (2) parameter names as listed in pydypackets.cfg
#  (3) their defaults
#  (4) whether these variables need to be converted to a boolean
param_guide = [ #section  #parameter #default #boolean?
              [ 'serial', 'port', "17", False],
              [ 'serial', 'baud', "1000000", False],
              [ 'default_device_type', 'AX-12', False, False]
              # [ '', '' , False, True ],
              # [ '', '' , False, True ],
              # [ '', '', True, True ]
              ]

param_list = list()

for param in param_guide:
    try:
        if config.has_section(param[0]):
        # Try to read from pydypackets.cfg
            param_list.append( config.get('r2s-params', param[1]) )
            if param[3]:
                param_list[-1] = bool(int(param_list[-1]))
    except ConfigParser.NoOptionError:
        # Use default
        param_list.append( param[2])

(port, baud) = param_list

