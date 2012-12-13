###WORK IN PROGRESS

import ConfigParser

config = ConfigParser.ConfigParser()

# Either pydypackets.cfg or pydypackets.txt are valid config files.
status = config.read("pydypackets.cfg")
if status == []:
    status = config.read("pydypackets.txt")
if status == []:
    print "ERROR: no config file exists. Create a pydypackets.cfg file in the " \
            "Config/ folder. See Config/config_example.cfg for more info."
    sys.exit()
    

# Read in other bot profile(s) (overwrite the initial configs that both
#  files define;)
if config.has_section("bots"):
    for profile in config.items("bots"):
        config.read(profile[1]) # UNTESTED

# Create device ID to device type dictionary
if config.has_section("id_to_device_type"):
    id_dict = dict([ (int(x[0]), x[1]) for x in \
            config.items("id_to_device_type")])
else:
    id_dict = dict([ ("default_device_type", "AX-12") ])
    
    
# This list stores (1) parameter names as listed in r2s.cfg; (2) their defaults;
# (3) whether these variables need to be converted to a boolean.
param_guide = [ #parameter #default #boolean?
        [ '', 'photon_isotope', "TOTAL", False],
        [ '', 'photon_cooling', 0, False],
        [ '', 'sampling' , 'v', False],
        [ '', 'custom_ergbins', False, True ],
        [ '', 'photon_bias' , False, True ],
        [ '', 'cumulative' , False, True ],
        [ '', 'add_fmesh_card', True, True ]
        ]

param_list = list()

for param in param_guide:
    try:
        # Try to read from r2s.cfg
        param_list.append( config.get('r2s-params', param[0]) )
        if param[2]:
            param_list[-1] = bool(int(param_list[-1]))
    except ConfigParser.NoOptionError:
        # Use default
        param_list.append( param[1])

(opt_isotope, opt_cooling, opt_sampling, opt_ergs, opt_bias, opt_cumulative, opt_phtnfmesh) = param_list

