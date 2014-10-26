#

from ConfigParser import ConfigParser


class PyDyConfigException(Exception):
    pass


class PyDyConfigParser(ConfigParser):

    def __init__(self):
        ConfigParser.__init__(self)
        #super(ConfigParser, self).__init__()
        #self.config = ConfigParser.ConfigParser()


    def read(self, myfile=None):
        """Invokes `get_config_file` to look for a config file if one
        was not supplied.

        Parameters
        ----------
        myfile : string, optional
            Path to config file to read.
        """
        self.get_config_file(myfile)


    def get_config_file(self, myfile=None):
        """Looks for configfile in current directory or in folder Config/.

        Parameters
        ----------
        myfile : string, optional
            Path to config file to read.
        """
        # Look for a config file if one was not supplied
        # Either pydypackets.cfg or pydypackets.txt are valid config files.
        if not myfile:
            configfilenames = [
                    "pydypackets.cfg",
                    "pydypackets.txt",
                    "Config/pydypackets.cfg",
                    "Config/pydypackets.txt",
                    ]
            for filename in configfilenames:
                status = ConfigParser.read(self, filename)#"Config/pydypackets.cfg")
                if status != []:
                    break
        else:
            status = ConfigParser.read(self, myfile)#"Config/pydypackets.cfg")

        if status == []:
            #print "\nERROR: no config file exists. Create a pydypackets.cfg file in " \
            #        "the Config/ folder. See Config/config_example.cfg for more info."
            #print "\nFor PyDyPackets usage guide, and more info, see 'Readme.rst'."
            msg = "ERROR: no config file exists. Create a pydypackets.cfg file in " \
                    "this folder by running `pydysetup`."
            raise PyDyConfigException(msg)

        #######################################
        # Read in other bot profile(s) (overwrites any configs that both
        #  files define)
        # TODO: UNTESTED
        if self.has_section("bots"):
            for profile in self.items("bots"):
                ConfigParser.read(self, profile[1])
    

    def get_params(self):
        """Gets parameters in several sections of config file and returns their
        values as a list.

        Returns
        -------
        tuple of assorted values
            Currently:
            port, baud, default_device_type, timing, include_timestamp_in_translate
        """
        # Grab single value parameters

        # The param_guide list stores
        #  (1) section containing parameter in pydypackets.cfg
        #  (2) parameter names as listed in pydypackets.cfg
        #  (3) their defaults
        #  (4) which 'get' function to use for the parameter
        param_guide = [ #sectionname #parametername #defaultvalue #getfunction
                      [ 'serial', 'port', "17", self.get],
                      [ 'serial', 'baud', "1000000", self.get],
                      [ 'default_device_type', 'default_device_type', 'AX-12', self.get],
                      [ 'timing', 'timing' , False, self.getboolean ],
                      [ 'translation', 'timestamp' , False, self.getboolean]
                      # [ '', '', True, self.get]
                      ]
            
        param_list = list()

        for param in param_guide:
            try:
                # Try to read from pydypackets.cfg
                if self.has_section(param[0]):
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

        self.default_device_type = default_device_type

        return port, baud, default_device_type, timing, include_timestamp_in_translate

        
    def get_id_to_device_dict(self):
        """Retrieves mapping of servo IDs to servo types.

        Returns
        -------
        id_dict : dictionary
            Mapping of servo ID #s (int) to servo types.

        Note
        ----
        Before invoking this method, :func:`get_params` must have been invoked.
        """
        if not hasattr(self, "default_device_type"):
            self.get_params()
        # Create device ID to device type dictionary
        if self.has_section("id_to_device_type"):
            try:
                id_dict = dict([ (int(x[0]), x[1]) for x in \
                        self.items("id_to_device_type")])
            except ValueError:
                print "\nERROR: IDs in section [id_to_device_type] of " \
                        "'Config/pydypackets.cfg' must be integers."
                exit()
        else:
            id_dict = dict()
            
        id_dict["default_device_type"] = self.default_device_type
        id_dict[None] = self.default_device_type
        # We fill out the list of non-defined IDs with the default
        #  (This avoids needing try-except everty time id_dict is used)
        for i in xrange(0,255):
            if i not in id_dict.keys():
                id_dict[i] = self.default_device_type

        return id_dict


    def get_limits(self):
        """Not implemented"""
        # Create device ID to device type dictionary
        if self.has_section("limits"):
            #id_dict = dict([ (int(x[0]), x[1]) for x in \
            #        self.items("id_to_device_type")])
            pass
        else:
            pass
            #id_dict = dict([ ("default_device_type", "AX-12") ])
        #return


    def get_plot_config(self):
        """A gets the matplotlib plot layout options from config file.

        Returns
        -------
        subplot_dict : dictionary
            A custom dictionary with keys starting from 0.  Each key
            corresponds with a subplot specification.  Typically, these defines
            a 3-digit subplot value, where digits are (1) # columns; (2) # rows;
            (3) plotnum. Plotnum goes row by row, filling columns of each row.
            You can specify this dictionary when calling plot_trends, or just
            modify dict_subplot in PyDyPlotter.py.
            See also:
            http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.subplot

        """
        # Get plotting layout information
        if self.has_section("plotting"):
            dict_subplot = dict([ (int(x[0]), int(x[1])) for x in \
                    self.items("plotting")])
            return dict_subplot
        else:
            return None
