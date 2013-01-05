Summary
----------------
The scripts in this repo are for reading, storing, parsing, filtering and plotting the byte-packets used for communication by the Dynamixel series of digital servos created by Robotis.

The scripts currently can handle the full instruction set used for talking `to` Dynamixel servos, and supports the settings for various Dynamixel devices.  Currently supported devices are:  

AX-12, AX-12W, AX-18, AX-S1, RX-24, RX-28, RX-64, MX-28, MX-64, MX-106, EX-106

The Scripts
-------------
There are six scripts with different purposes, and which use each other to various extents.  These are divided into two groups; those that the user interacts with, and those that are used internally.

User-friendly:

:``PyDyLogger.py``: Monitoring serial port and saving packets to file
:``PyDyParser.py``: Filtering lists of packets by ID, instruction, or command bytes
:``PyDyPlotter.py``: Creating plots from packets; e.g. plots of each servo's position

Each of these scripts can be called from the command line with various options.  For more info, try ``ScriptName.py -h``

Internal stuff:

:``PyDyPackets.py``: Translation, reference data, packet operations
:``PyDyConfig.py``: Parses the config file(s) in ``Config/``.
:``PyDyDevices.py``: Stores translation tables for different devices.

Usage
-----
The first thing that needs to be done is to create a config file.  To do this you can copy ``Config/config_example.cfg`` to ``Config/pydypackets.cfg``.  The latter is a required name.  An error is given if this file does not exist.

Within the config file, various settings can be found.  To start, set the serial/COM port being used for your setup.  Note that the port specification is OS dependent.  Once you have a config file, you can run stuff!

The steps for a couple of envisioned typical use cases are:

(1) Connect computer to a Dynamixel bus, and save bytes using ``PyDyLogger.py``
(2) Feed the output file into ``PyDyParser.py`` with various flags (``-t`` -> human readable output)
(3) Read the filtered output file in a text editor

Or:

1) Connect computer to a Dynamixel bus, and save bytes using ``PyDyLogger.py``
2) Feed the output file into ``PyDyPlotter.py`` with various flags and diagnose problems via plots

Requirements
----------------
Python (2.6+?) should be installed.  

Plotting capabilities use MatPlotLib.

http://matplotlib.org/

Origin/Purpose
----------------
Derived from needs discussed here:

http://forums.trossenrobotics.com/showthread.php?5670-Dynamixel-packet-analyzer

Relevant/Related Projects
------------------------------
https://github.com/RyanLowerr/Dynamixel-Python