Summary
-------
The scripts in this repo are for reading, storing, parsing, filtering and plotting the byte-packets used for communication by the Dynamixel series of digital servos created by Robotis.

The scripts currently can handle the full instruction set used for talking *to* Dynamixel servos, and supports the settings for various Dynamixel devices.  Currently supported devices are:  

AX-12, AX-12W, AX-18, AX-S1, RX-24, RX-28, RX-64, MX-28, MX-64, MX-106, EX-106

The Scripts
-----------
There are four scripts with different purposes, and which use each other to various extents.
These are divided into two groups; those that the user interacts with, and those that are used internally.

User-friendly:

:``pydysetup``: Sets up a directory for use of the other scripts by creating a default pydypackets.cfg file.
:``pydylogger``: Monitoring serial port and saving packets to file
:``pydyparser``: Filtering lists of packets by ID, instruction, or command bytes
:``pydyplotter``: Creating plots from packets; e.g. plots of each servo's position

Each of these scripts can be called from the command line with various options.
For more info, try ``ScriptName -h``

Usage
-----
This software should be installed as a package for Python 2.7.
To do this, download/clone the repository, and then run::

        python setup.py install
        
(If you are on Windows, make sure that ``C:\Python27\Scripts`` is in your PATH variable)

The first thing that needs to be done is to create a config file. To do this
invoke ``pydysetup``, which will create ``pydypackets.cfg`` in your current directory.
The other scripts will raise an error if this file does not exist in the current directory
or in a subfolder named ``Config``. (Having a global config file is on the TODO list.)

Within the config file, various settings can be found. To start,
set the serial/COM port being used for your setup. Note that the port
specification is OS dependent. Once you have a config file, you can run stuff!

The steps for a couple of envisioned typical use cases are:

(1) Connect computer to a Dynamixel bus, and save bytes using ``PyDyLogger.py``
(2) Feed the output file into ``PyDyParser.py`` with various flags (``-t`` -> human readable output)
(3) Read the filtered output file in a text editor

Or:

1) Connect computer to a Dynamixel bus, and save bytes using ``PyDyLogger.py``
2) Feed the output file into ``PyDyPlotter.py`` with various flags and diagnose problems via plots

Requirements
----------------
Python 2.7 should be installed. (3.x is not supported)

You will need the following packages, installed e.g. via ``pip``:

* ``pyserial``

Plotting capabilities use MatPlotLib.

http://matplotlib.org/

Origin/Purpose
----------------
Derived from needs discussed here:

http://forums.trossenrobotics.com/showthread.php?5670-Dynamixel-packet-analyzer

Relevant/Related Projects
------------------------------
https://github.com/RyanLowerr/Dynamixel-Python
