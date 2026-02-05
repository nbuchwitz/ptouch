Connection Module
=================

The connection module provides connection implementations for USB and network communication with Brother P-touch printers.

.. automodule:: ptouch.connection
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

USB Device Selection
--------------------

When multiple USB printers are connected, you can select a specific device using:

* ``product_id`` - USB product ID to match a specific printer model
* ``serial`` - USB serial number to match a specific device

Example:

.. code-block:: python

   from ptouch import ConnectionUSB

   # Connect to specific device by serial number
   connection = ConnectionUSB(product_id=0x2086, serial="A1B2C3D4E5")

USB URI Format
~~~~~~~~~~~~~~

The ``parse_usb_uri`` function parses USB device URIs for CLI usage:

.. code-block:: python

   from ptouch import parse_usb_uri

   # Parse various URI formats
   vendor, product, serial = parse_usb_uri("usb://0x04f9:0x2086/A1B2C3D4E5")
   vendor, product, serial = parse_usb_uri("usb://:0x2086/A1B2C3D4E5")
   vendor, product, serial = parse_usb_uri("usb://:0x2086")

Supported formats:

* ``usb://vendor:product`` - Vendor and product ID
* ``usb://vendor:product/serial`` - With serial number
* ``usb://:product`` - Product ID only (default vendor)
* ``usb://:product/serial`` - Product and serial (default vendor)

Exception Classes
-----------------

The module defines a hierarchy of exception classes for connection errors:

* ``PrinterConnectionError`` - Base exception for all connection errors
* ``PrinterNotFoundError`` - Printer device not found
* ``PrinterPermissionError`` - Permission denied (USB requires sudo/udev rules)
* ``PrinterNetworkError`` - Network connection/communication errors
* ``PrinterTimeoutError`` - Connection or operation timeout
* ``PrinterWriteError`` - Failed to write data to printer

All specific exceptions inherit from ``PrinterConnectionError``, allowing you to catch all connection-related errors with a single except clause.

See Also
--------

* :doc:`../quickstart` - Basic connection examples
* :doc:`../userguide` - Connection management patterns
* :doc:`exceptions` - Exception handling details
