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

Quick Start
-----------

.. code-block:: python

   from ptouch import ConnectionNetwork, PTP900, TextLabel, LaminatedTape36mm
   
   connection = ConnectionNetwork("192.168.1.100")
   printer = PTP900(connection, high_resolution=True)
   
   label = TextLabel("Hello World", LaminatedTape36mm, 
                     font="/path/to/font.ttf")
   printer.print(label)

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/connection
   api/printer
   api/label
   api/tape
   api/exceptions

Connection Module
-----------------

.. automodule:: ptouch.connection
   :members:
   :undoc-members:
   :show-inheritance:

Printer Module
--------------

.. automodule:: ptouch.printer
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: ptouch.printers
   :members:
   :undoc-members:
   :show-inheritance:

Label Module
------------

.. automodule:: ptouch.label
   :members:
   :undoc-members:
   :show-inheritance:

Tape Module
-----------

.. automodule:: ptouch.tape
   :members:
   :undoc-members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
