Summary
----------------
The scripts in this repo are for reading, storing, parsing, filtering and plotting the byte-packets used for communication by the Dynamixel series of digital servos.

Usage
-----
There are four scripts with different purposes, and which use each other to an extent:
-PyDyPackets.py: Translation, reference data, packet operations
-PyDyLogger.py: Monitoring serial port and saving packets to file
-PyDyParser.py: Filtering lists of packets by ID, instruction, or command bytes
-PyDyPlotter.py: Creating plots from packets; e.g. plots of each servo's position

Each of these scripts can be called from the command line with various options.  For more info, try 'ScriptName.py -h'

A couple typical envisioned use cases are:
1) Connect computer to a Dynamixel bus, and save bytes using PyDyLogger.py
2) Feed the output file into PyDyParser.py with various flags (-t -> human readable output)
3) Read the filtered output file

or
1) Connect computer to a Dynamixel bus, and save bytes using PyDyLogger.py
2) Feed the output file into PyDyPlotter.py with various flags and diagnose problems via plots

Origin/Purpose
--------
Derived from needs discussed here: http://forums.trossenrobotics.com/showthread.php?5670-Dynamixel-packet-analyzer