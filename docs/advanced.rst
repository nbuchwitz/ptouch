Advanced Topics
===============

This guide covers advanced features and optimization techniques.

High Resolution Mode
--------------------

Understanding Resolution
~~~~~~~~~~~~~~~~~~~~~~~~~

Each printer supports two resolution modes:

* **Standard resolution**: 180 DPI (E550W, P750W) or 360 DPI (P900 series)
* **High resolution**: 360 DPI (E550W, P750W) or 720 DPI (P900 series)

High resolution mode doubles the vertical resolution, resulting in:

* Sharper text and graphics
* Smoother curves and diagonals
* ~2x slower printing
* Same tape length used

When to Use High Resolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use high resolution for:

* Small text (< 12pt)
* QR codes and barcodes
* Detailed logos or graphics
* Professional-looking labels

Standard resolution is sufficient for:

* Large text (> 18pt)
* Simple graphics
* Cable labels and asset tags
* When speed matters

Enabling High Resolution
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # At printer initialization (applies to all prints)
   printer = PTP900(connection, high_resolution=True)

   # Per print job
   printer = PTP900(connection)
   printer.print(label, high_resolution=True)

   # Command line
   ptouch "High Quality" --high-resolution --host 192.168.1.100 \
       --printer P900 --tape-width 36

TIFF Compression
----------------

How It Works
~~~~~~~~~~~~

The library uses PackBits compression (TIFF) to reduce data transfer:

* Compresses each raster line independently
* Typical compression ratio: 50-80% for text labels
* Especially effective for labels with large white areas
* Minimal CPU overhead

Performance Impact
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time

   # With compression (default)
   start = time.time()
   printer.print(label, use_compression=True)
   compressed_time = time.time() - start

   # Without compression
   start = time.time()
   printer.print(label, use_compression=False)
   uncompressed_time = time.time() - start

   print(f"Compression saved {uncompressed_time - compressed_time:.2f}s")

Disabling Compression
~~~~~~~~~~~~~~~~~~~~~~

Disable if encountering issues or for troubleshooting:

.. code-block:: python

   printer.print(label, use_compression=False)

Lazy Connection Initialization
-------------------------------

Connections are established lazily on first use:

.. code-block:: python

   # Connection object created, but not yet connected
   connection = ConnectionNetwork("192.168.1.100")

   # Actual connection happens here
   printer = PTP900(connection)
   printer.print(label)  # Connects if needed

This pattern allows:

* Fast initialization
* Error handling at print time
* Connection pooling strategies

Manual Connection Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import ConnectionNetwork, PrinterTimeoutError

   connection = ConnectionNetwork("192.168.1.100")
   printer = PTP900(connection)

   # Retry logic
   max_retries = 3
   for attempt in range(max_retries):
       try:
           printer.print(label)
           break
       except PrinterTimeoutError:
           if attempt == max_retries - 1:
               raise
           print(f"Retry {attempt + 1}/{max_retries}...")
           time.sleep(1)

Image Processing
----------------

Optimal Image Format
~~~~~~~~~~~~~~~~~~~~

For best results:

* **Format**: PNG or JPEG
* **Color mode**: RGB or Grayscale (converted to 1-bit internally)
* **Resolution**: Match printer DPI (360 or 720)
* **Height**: Match tape's printable area

Calculating Image Dimensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def calculate_dimensions(tape_width_mm, label_width_mm, dpi=360):
       """Calculate image dimensions for given tape and label width."""
       # Printable area varies by tape width
       printable_areas = {
           6: 32,   # 32 pins / ~2.3mm
           9: 50,   # 50 pins / ~3.5mm
           12: 70,  # 70 pins / ~4.9mm
           18: 112, # 112 pins / ~7.9mm
           24: 128, # 128 pins / ~9.0mm
           36: 454, # 454 pins / ~31.8mm (at 360 DPI)
       }

       height_pixels = printable_areas.get(tape_width_mm, 128)
       width_pixels = int(label_width_mm * dpi / 25.4)

       return width_pixels, height_pixels

   # Create optimally sized image
   width, height = calculate_dimensions(36, 60, dpi=360)
   img = Image.new("RGB", (width, height), "white")

Image Dithering
~~~~~~~~~~~~~~~

For grayscale images, apply dithering for better results:

.. code-block:: python

   from PIL import Image

   # Load grayscale image
   img = Image.open("photo.jpg").convert("L")

   # Apply Floyd-Steinberg dithering
   img = img.convert("1", dither=Image.FLOYDSTEINBERG)

   # Print
   label = Label(img.convert("RGB"), LaminatedTape36mm)
   printer.print(label)

Batch Processing Optimization
------------------------------

Efficient Multi-Label Printing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def print_labels_efficiently(printer, label_data):
       """Print multiple labels with optimized settings."""
       labels = []

       # Pre-generate all labels
       for data in label_data:
           label = create_label(data)  # Your label creation function
           labels.append(label)

       # Print in single job with half-cuts
       printer.print_multi(labels, half_cut=True)

Network Optimization
--------------------

Connection Timeout Tuning
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import socket

   connection = ConnectionNetwork("192.168.1.100")

   # Access underlying socket (after connection established)
   printer = PTP900(connection)
   printer.print(first_label)  # Establishes connection

   # Adjust timeout
   if hasattr(connection, '_socket'):
       connection._socket.settimeout(30.0)  # 30 second timeout

Keep-Alive for Long Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def print_with_keepalive(printer, labels):
       """Print with connection keep-alive."""
       for idx, label in enumerate(labels):
           try:
               printer.print(label)
           except PrinterTimeoutError:
               # Reconnect and retry
               print(f"Reconnecting at label {idx}...")
               printer = PTP900(ConnectionNetwork("192.168.1.100"))
               printer.print(label)

Custom Raster Data
------------------

Advanced: Direct Raster Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For complete control over raster data:

.. code-block:: python

   from ptouch.printer import LabelPrinter

   # Access internal methods (use with caution)
   tape_config = printer.get_tape_config(LaminatedTape36mm)

   # Generate custom raster data
   # Each line must be tape_config.print_pins bits
   raster_data = generate_custom_raster()  # Your function

   # Build and send raster commands
   # Note: This is internal API and may change
   commands = printer._build_raster_data(
       raster_data,
       num_lines=len(raster_data) // tape_config.bytes_per_line,
       high_res=True
   )

Best Practices
--------------

Performance Tips
~~~~~~~~~~~~~~~~

1. **Reuse connections** - Don't create new connections per label
2. **Batch prints** - Use ``print_multi()`` when printing multiple labels
3. **Pre-generate labels** - Separate generation from printing
4. **Use standard resolution** - Unless quality demands high-res
5. **Enable compression** - Faster data transfer (default)
6. **Optimize images** - Match printer DPI, use 1-bit color when possible

Quality Tips
~~~~~~~~~~~~

1. **Use high resolution** - For small text and detailed graphics
2. **Test fonts** - Not all fonts render well at all sizes
3. **Proper DPI** - Match image resolution to printer
4. **Consider tape width** - Larger tape = more detail possible
5. **Apply dithering** - For grayscale/photo images

Reliability Tips
~~~~~~~~~~~~~~~~

1. **Always handle errors** - Network/USB can fail
2. **Implement retries** - For transient failures
3. **Verify tape type** - Wrong configuration causes misalignment
4. **Check printer status** - Before large batch jobs
5. **Test first** - Print one label before batch job

Next Steps
----------

* :doc:`adding_devices` - Extend library with new printers
* :doc:`troubleshooting` - Solve common problems
* :doc:`api/printer` - API reference documentation
