#

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
# Read in other bot profile(s) (overwrites any configs that both
#  files define)
if config.has_section("bots"):
    for profile in config.items("bots"):
        config.read(profile[1]) # UNTESTED
    
#######################################
# Grab single value parameters

# This list stores 
#  (1) section containing parameter in pydypackets.cfg
#  (2) parameter names as listed in pydypackets.cfg
#  (3) their defaults
#  (4) which 'get' function to use for the parameter
param_guide = [ #sectionname #parametername #defaultvalue #getfunction
              [ 'serial', 'port', "17", config.get],
              [ 'serial', 'baud', "1000000", config.get],
              [ 'default_device_type', 'default_device_type', 'AX-12', config.get],
              [ 'timing', 'timing' , False, config.getboolean ],
              [ 'translation', 'timestamp' , False, config.getboolean]
              # [ '', '', True, config.get]
              ]
    
param_list = list()

for param in param_guide:
    try:
        if config.has_section(param[0]):
        # Try to read from pydypackets.cfg
            # Note that param[3] is a function
            param_list.append( param[3](param[0], param[1]) )
    except ConfigParser.NoOptionError:
        # Use default
        param_list.append( param[2])

(port, baud, default_device_type, timing, include_timestamp_in_translate, ) = param_list

try:
    port = int(port)
except ValueError:
    pass # Non-numeric port specification

#######################################
# Create device ID to device type dictionary
if config.has_section("id_to_device_type"):
    try:
        id_dict = dict([ (int(x[0]), x[1]) for x in \
                config.items("id_to_device_type")])
    except ValueError:
        print "\nERROR: IDs in section [id_to_device_type] of " \
                "'Config/pydypackets.cfg' must be integers."
        exit()
else:
    id_dict = dict()
    
id_dict["default_device_type"] = default_device_type
id_dict[None] = default_device_type
# We fill out the list of non-defined IDs with the default
#  (This avoids needing try-except everty time id_dict is used)
for i in xrange(0,255):
    if i not in id_dict.keys():
        id_dict[i] = default_device_type

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
