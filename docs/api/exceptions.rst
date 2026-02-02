Exceptions
==========

The ptouch library provides a hierarchy of exception classes for targeted error handling.

Exception Hierarchy
-------------------

All printer-related exceptions inherit from ``PrinterConnectionError``:

.. code-block:: text

   PrinterConnectionError (base)
   ├── PrinterNotFoundError
   ├── PrinterPermissionError
   ├── PrinterNetworkError
   ├── PrinterTimeoutError
   └── PrinterWriteError

Exception Classes
-----------------

.. py:exception:: PrinterConnectionError

   Base exception for all printer connection errors.

   **Attributes:**

   * ``original_error`` - The original exception that caused this error (if any)

   **Usage:**

   Catch this exception to handle all connection-related errors:

   .. code-block:: python

      try:
          printer.print(label)
      except PrinterConnectionError as e:
          print(f"Connection error: {e}")
          if e.original_error:
              print(f"Original error: {e.original_error}")

.. py:exception:: PrinterNotFoundError

   Printer device not found or not accessible.

   **Common causes:**

   * USB printer not connected
   * Wrong USB product ID
   * Device unplugged during operation

   **Solutions:**

   * Check USB connection
   * Verify printer is powered on
   * Check product ID matches your model

.. py:exception:: PrinterPermissionError

   Insufficient permissions to access printer (USB only).

   **Common causes:**

   * Linux USB permissions not configured
   * Running without necessary privileges

   **Solutions:**

   See :doc:`../installation` for USB permissions setup (udev rules, user groups).

.. py:exception:: PrinterNetworkError

   Network-specific connection errors.

   **Common causes:**

   * Network connectivity issues
   * Firewall blocking port 9100
   * Printer disconnected from network
   * Connection lost during print

   **Solutions:**

   * Check network connectivity
   * Verify firewall settings
   * Test with ``telnet <ip> 9100``
   * Check WiFi signal strength

.. py:exception:: PrinterTimeoutError

   Connection or operation timeout.

   **Common causes:**

   * Printer powered off
   * Wrong IP address
   * Network latency
   * Printer busy or jammed

   **Solutions:**

   * Verify printer is powered on
   * Check IP address is correct
   * Increase timeout if needed
   * Check printer status (paper, cover, etc.)

.. py:exception:: PrinterWriteError

   Failed to write data to printer.

   **Common causes:**

   * USB cable disconnected
   * USB communication error
   * Network connection lost
   * Incomplete data transfer

   **Solutions:**

   * Check USB/network connection
   * Try different USB port or cable
   * Implement retry logic
   * Check for transient errors

Usage Examples
--------------

Catch All Connection Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import PrinterConnectionError

   try:
       printer.print(label)
   except PrinterConnectionError as e:
       print(f"Failed to print: {e}")

Catch Specific Errors
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import (
       PrinterTimeoutError,
       PrinterNetworkError,
       PrinterPermissionError,
   )

   try:
       printer.print(label)
   except PrinterPermissionError:
       print("Permission denied - see installation guide for USB setup")
   except PrinterTimeoutError:
       print("Printer not responding - check if powered on")
   except PrinterNetworkError as e:
       print(f"Network error: {e} - check connectivity")

Access Original Error
~~~~~~~~~~~~~~~~~~~~~

All exceptions preserve the original error:

.. code-block:: python

   try:
       printer.print(label)
   except PrinterConnectionError as e:
       print(f"Error: {e}")
       if e.original_error:
           print(f"Caused by: {type(e.original_error).__name__}")
           print(f"Details: {e.original_error}")

Retry Logic
~~~~~~~~~~~

Implement retry logic for transient failures:

.. code-block:: python

   import time
   from ptouch import PrinterTimeoutError, PrinterNetworkError

   def print_with_retry(printer, label, max_retries=3):
       for attempt in range(max_retries):
           try:
               printer.print(label)
               return True
           except (PrinterTimeoutError, PrinterNetworkError) as e:
               if attempt == max_retries - 1:
                   raise
               print(f"Retry {attempt + 1}/{max_retries}: {e}")
               time.sleep(2)
       return False

Best Practices
--------------

1. **Always catch PrinterConnectionError** - Use specific exceptions for known scenarios, fall back to base exception

2. **Log original errors** - The ``original_error`` attribute helps debugging

3. **Provide user feedback** - Give actionable error messages:

   .. code-block:: python

      except PrinterTimeoutError:
          print("Printer not responding:")
          print("  1. Check if printer is powered on")
          print("  2. Verify network connection")
          print("  3. Check IP address is correct")

4. **Implement retries** - Network and USB connections can have transient failures

5. **Check permissions early** - Test USB permissions before batch jobs:

   .. code-block:: python

      from ptouch import ConnectionUSB, PrinterPermissionError

      try:
          connection = ConnectionUSB()
          # Test connection
          printer = PTE550W(connection)
      except PrinterPermissionError:
          print("USB permissions not configured")
          print("See: https://ptouch.readthedocs.io/en/latest/installation.html")
          sys.exit(1)

See Also
--------

* :doc:`../troubleshooting` - Solutions to common problems
* :doc:`../installation` - USB permissions setup
* :doc:`connection` - Connection module documentation
