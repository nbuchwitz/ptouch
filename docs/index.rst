ptouch - Brother P-touch Label Printer Library
===============================================

A Python library for Brother P-touch label printers with support for USB and network connections.

Features
--------

* Support for multiple Brother P-touch models (PT-E550W, PT-P750W, PT-P900 series)
* Network (TCP/IP) and USB connections
* Text labels with customizable fonts and alignment
* Image label printing
* Multi-label printing with half-cut support
* High resolution mode support
* TIFF compression for efficient data transfer
* Comprehensive error handling with specific exception types

Installation
------------

.. code-block:: bash

   pip install ptouch        # Basic installation
   pip install ptouch[usb]   # With USB support

Quick Example
-------------

.. code-block:: python

   from ptouch import ConnectionNetwork, PTP900, TextLabel, LaminatedTape36mm
   from PIL import ImageFont

   connection = ConnectionNetwork("192.168.1.100")
   printer = PTP900(connection, high_resolution=True)

   font = ImageFont.load_default()
   label = TextLabel("Hello World", LaminatedTape36mm, font=font)
   printer.print(label)

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   userguide
   examples
   advanced
   adding_devices
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/connection
   api/printer
   api/label
   api/tape
   api/exceptions

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
