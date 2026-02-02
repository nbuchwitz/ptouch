Connection Module
=================

The connection module provides connection implementations for USB and network communication with Brother P-touch printers.

.. automodule:: ptouch.connection
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

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
