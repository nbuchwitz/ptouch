Quick Start
===========

This guide will help you print your first label in under 5 minutes.

Your First Label
----------------

Network Connection
~~~~~~~~~~~~~~~~~~

The simplest way to get started is with a network-connected printer:

.. code-block:: python

   from ptouch import ConnectionNetwork, PTP900, TextLabel, Tape36mm
   from PIL import ImageFont

   # Connect to printer
   connection = ConnectionNetwork("192.168.1.100")
   printer = PTP900(connection, high_resolution=True)

   # Create text label
   font = ImageFont.load_default()  # Use PIL's default font
   label = TextLabel("Hello World", Tape36mm, font=font)

   # Print!
   printer.print(label)
   print("Label printed successfully")

USB Connection
~~~~~~~~~~~~~~

For USB-connected printers:

.. code-block:: python

   from ptouch import ConnectionUSB, PTE550W, TextLabel, Tape12mm
   from PIL import ImageFont

   # Connect via USB (finds first available Brother printer)
   connection = ConnectionUSB()
   printer = PTE550W(connection)

   # Create and print label
   font = ImageFont.load_default()
   label = TextLabel("Hello USB", Tape12mm, font=font)
   printer.print(label)

Using the Command Line
----------------------

The library includes a command-line interface:

.. code-block:: bash

   # Print text label
   ptouch "Hello World" --host 192.168.1.100 --printer P900 --tape-width 36

   # Print with custom font
   ptouch "Custom Font" --host 192.168.1.100 --printer P900 \
       --tape-width 36 --font /path/to/font.ttf --high-resolution

   # Print image
   ptouch --image logo.png --host 192.168.1.100 --printer P900 --tape-width 36

   # Print multiple labels (half-cut between, saves tape)
   ptouch "Label 1" "Label 2" "Label 3" --host 192.168.1.100 \
       --printer P900 --tape-width 12

Understanding the Basics
-------------------------

The library provides printer classes for different Brother P-touch models (``PTE550W``, ``PTP750W``, ``PTP900``, etc.) and tape types (``Tape3_5mm`` through ``Tape36mm``). See :doc:`api/printer` for complete printer specifications and :doc:`api/tape` for tape compatibility.

Error Handling
--------------

The library provides specific exception types for different error scenarios. See :doc:`api/exceptions` for complete exception hierarchy and :doc:`troubleshooting` for solving common problems.

Next Steps
----------

* :doc:`userguide` - Detailed guide with more examples
* :doc:`examples` - Real-world usage examples
* :doc:`advanced` - High-resolution mode, compression, and more
