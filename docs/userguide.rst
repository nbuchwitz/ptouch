User Guide
==========

This guide covers common use cases and patterns for the ptouch library.

Text Labels
-----------

Basic Text Label
~~~~~~~~~~~~~~~~

Create a simple text label with default settings:

.. code-block:: python

   from ptouch import ConnectionNetwork, PTP900, TextLabel, LaminatedTape36mm
   from PIL import ImageFont

   connection = ConnectionNetwork("192.168.1.100")
   printer = PTP900(connection)

   font = ImageFont.load_default()
   label = TextLabel("Hello World", LaminatedTape36mm, font=font)
   printer.print(label)

Custom Font and Size
~~~~~~~~~~~~~~~~~~~~

Use TrueType fonts with custom sizes:

.. code-block:: python

   from PIL import ImageFont

   # Load custom font with specific size
   font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)

   # Auto-sizing is disabled when font has explicit size
   label = TextLabel("Custom Font", LaminatedTape36mm, font=font, auto_size=False)

   # Or let the library auto-size to 80% of tape height
   label = TextLabel("Auto Sized", LaminatedTape36mm, font=font, auto_size=True)

Text Alignment
~~~~~~~~~~~~~~

Control horizontal and vertical alignment:

.. code-block:: python

   # Horizontal: LEFT, HCENTER, RIGHT
   # Vertical: TOP, VCENTER, BOTTOM
   # Combined: CENTER = HCENTER | VCENTER

   label = TextLabel(
       "Centered",
       LaminatedTape36mm,
       font=font,
       align=TextLabel.Align.CENTER  # Center both ways
   )

   label = TextLabel(
       "Top Left",
       LaminatedTape36mm,
       font=font,
       align=TextLabel.Align.LEFT | TextLabel.Align.TOP
   )

   label = TextLabel(
       "Bottom Right",
       LaminatedTape36mm,
       font=font,
       align=TextLabel.Align.RIGHT | TextLabel.Align.BOTTOM
   )

Fixed Width Labels
~~~~~~~~~~~~~~~~~~

Create labels with specific width:

.. code-block:: python

   # Create 50mm wide label (useful for consistent sizing)
   label = TextLabel(
       "Short",
       LaminatedTape36mm,
       font=font,
       width_mm=50.0
   )

Image Labels
------------

Basic Image Label
~~~~~~~~~~~~~~~~~

Print images directly:

.. code-block:: python

   from PIL import Image
   from ptouch import Label, LaminatedTape36mm

   # Load image
   image = Image.open("logo.png")

   # Create label and print
   label = Label(image, LaminatedTape36mm)
   printer.print(label, margin_mm=3.0)

Creating Custom Images
~~~~~~~~~~~~~~~~~~~~~~

Generate labels programmatically:

.. code-block:: python

   from PIL import Image, ImageDraw, ImageFont

   # Create blank image (360 DPI for P900)
   # 36mm tape = ~32mm printable = 454 pixels at 360 DPI
   width = 800  # Adjust as needed
   height = 454
   img = Image.new("RGB", (width, height), "white")
   draw = ImageDraw.Draw(img)

   # Draw content
   font = ImageFont.truetype("/path/to/font.ttf", 48)
   draw.text((10, 200), "Custom Label", font=font, fill="black")
   draw.rectangle([10, 10, 790, 444], outline="black", width=3)

   # Print
   label = Label(img, LaminatedTape36mm)
   printer.print(label)

QR Code Labels
~~~~~~~~~~~~~~

Create QR code labels:

.. code-block:: python

   import qrcode
   from PIL import Image

   # Generate QR code
   qr = qrcode.QRCode(version=1, box_size=10, border=4)
   qr.add_data("https://example.com")
   qr.make(fit=True)

   img = qr.make_image(fill_color="black", back_color="white")

   # Print
   label = Label(img.convert("RGB"), LaminatedTape36mm)
   printer.print(label)

Multi-Label Printing
---------------------

Print Multiple Labels Efficiently
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Save tape by using half-cuts between labels:

.. code-block:: python

   labels = [
       TextLabel("Server 1", LaminatedTape12mm, font=font),
       TextLabel("Server 2", LaminatedTape12mm, font=font),
       TextLabel("Server 3", LaminatedTape12mm, font=font),
   ]

   # Half-cut between labels (default), full cut after last
   printer.print_multi(labels)

   # Or use full cuts between all labels
   printer.print_multi(labels, half_cut=False)

Printing Multiple Copies
~~~~~~~~~~~~~~~~~~~~~~~~~

Command line:

.. code-block:: bash

   ptouch "Asset Tag" --copies 5 --host 192.168.1.100 \
       --printer P900 --tape-width 12

Python:

.. code-block:: python

   for i in range(5):
       label = TextLabel(f"Asset {i:03d}", LaminatedTape12mm, font=font)
       printer.print(label)

Connection Management
---------------------

Network Connection
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import ConnectionNetwork

   # Default port 9100
   connection = ConnectionNetwork("192.168.1.100")

   # Custom port
   connection = ConnectionNetwork("192.168.1.100", port=9100)

USB Connection
~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import ConnectionUSB

   # Find first available Brother printer
   connection = ConnectionUSB()

   # Specify vendor/product ID
   connection = ConnectionUSB(
       vendor_id=0x04f9,  # Brother
       product_id=0x20af  # PT-P900 series
   )

Print Settings
--------------

High Resolution Mode
~~~~~~~~~~~~~~~~~~~~

Enable high-resolution printing:

.. code-block:: python

   # Enable at printer initialization
   printer = PTP900(connection, high_resolution=True)

   # Or per print job
   printer = PTP900(connection)
   printer.print(label, high_resolution=True)

Margins
~~~~~~~

Adjust label margins:

.. code-block:: python

   # Default: 2mm margin
   printer.print(label)

   # Custom margin
   printer.print(label, margin_mm=5.0)

   # No margin
   printer.print(label, margin_mm=0.0)

Compression
~~~~~~~~~~~

TIFF compression is enabled by default for efficient data transfer:

.. code-block:: python

   # Disable compression (if needed)
   printer.print(label, use_compression=False)

Auto-Cut Control
~~~~~~~~~~~~~~~~

Control cutting behavior:

.. code-block:: python

   # Auto-cut enabled (default)
   printer.print(label, auto_cut=True)

   # No auto-cut (useful for continuous tape)
   printer.print(label, auto_cut=False)

Error Handling
--------------

Exception Hierarchy
~~~~~~~~~~~~~~~~~~~

The library provides specific exception types:

.. code-block:: python

   from ptouch import (
       PrinterConnectionError,     # Base exception
       PrinterNotFoundError,        # Device not found
       PrinterPermissionError,      # Permission denied (USB)
       PrinterNetworkError,         # Network errors
       PrinterTimeoutError,         # Timeout errors
       PrinterWriteError,           # Write failures
   )

Comprehensive Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   try:
       printer.print(label)
       print("Label printed successfully")

   except PrinterPermissionError:
       print("Permission denied")
       print("  Run with sudo or configure udev rules")
       print("  See: https://ptouch.readthedocs.io/en/latest/installation.html")

   except PrinterTimeoutError:
       print("Printer not responding")
       print("  - Check if printer is powered on")
       print("  - Verify network connection")
       print("  - Check IP address is correct")

   except PrinterNotFoundError:
       print("Printer not found")
       print("  - Check USB connection")
       print("  - Verify printer is powered on")
       print("  - Check product ID matches your model")

   except PrinterNetworkError as e:
       print(f"Network error: {e}")
       print("  - Check network connectivity")
       print("  - Verify firewall settings")

   except PrinterWriteError as e:
       print(f"Write error: {e}")
       print("  - Check USB cable")
       print("  - Try a different USB port")

   except PrinterConnectionError as e:
       print(f"General connection error: {e}")

Accessing Original Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~

All exceptions preserve the original error:

.. code-block:: python

   try:
       printer.print(label)
   except PrinterConnectionError as e:
       print(f"Error: {e}")
       if e.original_error:
           print(f"Original: {e.original_error}")

Next Steps
----------

* :doc:`examples` - Real-world usage examples
* :doc:`advanced` - Advanced features and optimizations
* :doc:`troubleshooting` - Common issues and solutions
