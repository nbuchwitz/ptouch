Troubleshooting
===============

This guide covers common problems and their solutions.

Connection Issues
-----------------

"Printer not responding" (Network)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**

* ``PrinterTimeoutError`` exception
* No response from printer

**Solutions:**

1. **Verify printer is powered on and connected to network**

   .. code-block:: bash

      ping 192.168.1.100

2. **Check IP address is correct**

   * Print network configuration from printer menu
   * Verify IP hasn't changed (use static IP or DHCP reservation)

3. **Check firewall settings**

   .. code-block:: bash

      # Linux: Allow port 9100
      sudo ufw allow 9100/tcp

      # Test with telnet
      telnet 192.168.1.100 9100

4. **Try different network**

   * Some networks block printer protocols
   * Corporate networks may require special configuration

5. **Increase timeout**

   .. code-block:: python

      connection = ConnectionNetwork("192.168.1.100")
      printer = PTP900(connection)

      # After first connection, adjust timeout
      printer.print(first_label)
      if hasattr(connection, '_socket'):
           connection._socket.settimeout(30.0)

"Permission denied" (USB)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**

* ``PrinterPermissionError`` exception
* ``usb.core.USBError: [Errno 13] Access denied (insufficient permissions)``

**Solutions:**

1. **Configure USB permissions** (recommended)

   See :doc:`installation` for detailed udev rules setup.

2. **Run with sudo** (not recommended)

   .. code-block:: bash

      sudo python your_script.py

"Printer not found" (USB)
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**

* ``PrinterNotFoundError`` exception
* No USB device found

**Solutions:**

1. **Verify USB connection**

   .. code-block:: bash

      lsusb | grep Brother
      # Should show: Bus 001 Device 010: ID 04f9:20af Brother Industries, Ltd

2. **Check product ID matches**

   .. code-block:: python

      import usb.core

      # List all Brother devices
      devices = usb.core.find(find_all=True, idVendor=0x04f9)
      for dev in devices:
          print(f"Product ID: {hex(dev.idProduct)}")

      # Compare with printer class USB_PRODUCT_ID

3. **Try different USB port**

   * Some USB hubs cause issues
   * Try direct connection to computer

4. **Check USB cable**

   * Try a different cable
   * Some cables are power-only

Network Error After Print Start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**

* Print starts but fails mid-job
* ``PrinterNetworkError`` during printing

**Solutions:**

1. **Check WiFi signal strength**

   * Move printer closer to access point
   * Use Ethernet instead of WiFi

2. **Implement retry logic**

   .. code-block:: python

      def print_with_retry(printer, label, max_retries=3):
          for attempt in range(max_retries):
              try:
                  printer.print(label)
                  return
              except PrinterNetworkError:
                  if attempt == max_retries - 1:
                      raise
                  print(f"Retry {attempt + 1}/{max_retries}...")
                  time.sleep(2)

Print Quality Issues
--------------------

Misaligned Labels
~~~~~~~~~~~~~~~~~

**Symptoms:**

* Content shifted up/down on tape
* Cut-off text or images

**Causes and Solutions:**

1. **Wrong tape type specified**

   .. code-block:: python

      # Wrong: Using 12mm tape but specified 24mm
      label = TextLabel("Text", LaminatedTape24mm, font=font)

      # Correct: Match actual tape in printer
      label = TextLabel("Text", LaminatedTape12mm, font=font)

2. **Wrong printer class**

   .. code-block:: python

      # Wrong: PT-E550W connected but using PT-P900 class
      printer = PTP900(connection)  # Wrong

      # Correct: Match actual printer model
      printer = PTE550W(connection)  # Correct

3. **Check tape is loaded correctly**

   * Remove and reinsert tape cassette
   * Ensure tape feeds smoothly

Blurry or Pixelated Text
~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**

* Text appears jagged or blurry
* Poor print quality

**Solutions:**

1. **Enable high resolution mode**

   .. code-block:: python

      printer = PTP900(connection, high_resolution=True)

2. **Use appropriate font size**

   * Small text (< 12pt) benefits from high-res mode
   * Very large text may look pixelated - use vector fonts

3. **Check image resolution**

   .. code-block:: python

      # Match printer DPI
      # P900: 360 DPI standard, 720 DPI high-res
      # E550W: 180 DPI standard, 360 DPI high-res

      def create_image_for_printer(width_mm, tape_mm, high_res=True):
          dpi = 720 if high_res else 360
          width_px = int(width_mm * dpi / 25.4)
          height_px = int(tape_mm * dpi / 25.4)
          return Image.new("RGB", (width_px, height_px), "white")

4. **Check print head**

   * Clean print head following manual instructions
   * Run printer's cleaning cycle

Incomplete Labels
~~~~~~~~~~~~~~~~~

**Symptoms:**

* Label cuts off at the end
* Missing content on right side

**Solutions:**

1. **Check label width calculation**

   .. code-block:: python

      # For text labels, auto-sizing should work
      label = TextLabel("Text", LaminatedTape12mm, font=font)  # Auto-sized

      # For image labels, ensure image isn't too wide
      max_width_mm = 100  # Adjust based on your needs
      width_px = int(max_width_mm * 360 / 25.4)

      # Resize if needed
      if img.width > width_px:
          aspect = img.height / img.width
          img = img.resize((width_px, int(width_px * aspect)))

2. **Increase margin**

   .. code-block:: python

      printer.print(label, margin_mm=5.0)

Vertical Lines in Print
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**

* White vertical lines in solid areas
* Uneven print density

**Causes:**

* Dirty print head
* Worn print head

**Solutions:**

1. Run printer's cleaning cycle (see manual)
2. Replace print head if worn (see manual)
3. Try different tape cassette to rule out tape issue

Software Issues
---------------

Import Errors
~~~~~~~~~~~~~

**Symptoms:**

* ``ModuleNotFoundError: No module named 'ptouch'``
* ``ImportError: cannot import name 'PTP900'``

**Solutions:**

1. **Verify installation**

   .. code-block:: bash

      pip list | grep ptouch
      # Should show: ptouch  1.0.0 (or similar)

2. **Reinstall package**

   .. code-block:: bash

      pip uninstall ptouch
      pip install ptouch

3. **Check Python version**

   .. code-block:: bash

      python --version
      # Requires Python 3.11 or later

4. **Virtual environment issues**

   .. code-block:: bash

      # Ensure you're in the correct venv
      which python
      pip install ptouch

Font Errors
~~~~~~~~~~~

**Symptoms:**

* ``OSError: cannot open resource``
* ``AttributeError: 'NoneType' object has no attribute 'getsize'``

**Solutions:**

1. **Use ImageFont.load_default()**

   .. code-block:: python

      from PIL import ImageFont

      # Simplest solution - always available
      font = ImageFont.load_default()

2. **Verify font file path**

   .. code-block:: python

      import os

      font_path = "/path/to/font.ttf"
      if not os.path.exists(font_path):
          print(f"Font not found: {font_path}")

      # Use absolute paths
      font = ImageFont.truetype(os.path.abspath(font_path), 48)

3. **Find system fonts**

   .. code-block:: bash

      # Linux
      fc-list : file | grep -i dejavu

      # macOS
      ls /System/Library/Fonts/
      ls ~/Library/Fonts/

      # Windows
      dir C:\\Windows\\Fonts

4. **Install fonts**

   .. code-block:: bash

      # Debian/Ubuntu
      sudo apt install fonts-dejavu

      # Fedora/RHEL
      sudo dnf install dejavu-fonts

Command Line Issues
-------------------

"ptouch: command not found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solutions:**

1. **Use python -m**

   .. code-block:: bash

      python -m ptouch "Hello World" --host 192.168.1.100 \
          --printer P900 --tape-width 36

2. **Check installation**

   .. code-block:: bash

      pip show ptouch
      # Look for "Location" line

      # Check if scripts directory is in PATH
      echo $PATH

3. **Reinstall with --force-reinstall**

   .. code-block:: bash

      pip install --force-reinstall ptouch

Wrong Arguments Error
~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**

* ``error: the following arguments are required``

**Solutions:**

1. **Check required arguments**

   .. code-block:: bash

      ptouch --help

      # Required: --host or --usb, --printer, --tape-width
      # Required: text or --image

2. **Common mistakes**

   .. code-block:: bash

      # Wrong: Missing connection
      ptouch "Text" --printer P900 --tape-width 36

      # Correct:
      ptouch "Text" --host 192.168.1.100 --printer P900 --tape-width 36

      # Wrong: Missing text
      ptouch --host 192.168.1.100 --printer P900 --tape-width 36

      # Correct:
      ptouch "Hello" --host 192.168.1.100 --printer P900 --tape-width 36

Performance Issues
------------------

Slow Printing
~~~~~~~~~~~~~

**Causes and Solutions:**

1. **High resolution mode enabled**

   * High-res doubles print time
   * Use standard resolution if quality permits

   .. code-block:: python

      printer = PTP900(connection, high_resolution=False)

2. **Large images**

   * Resize images to required dimensions
   * Don't use images larger than necessary

3. **Network latency**

   * Use USB instead of network if possible
   * Check network connection quality

4. **Compression disabled**

   * Enable compression (it's on by default)

   .. code-block:: python

      printer.print(label, use_compression=True)

5. **Individual prints instead of batch**

   .. code-block:: python

      # Slow: Individual prints
      for text in texts:
          label = TextLabel(text, LaminatedTape12mm, font=font)
          printer.print(label)

      # Fast: Batch printing
      labels = [TextLabel(t, LaminatedTape12mm, font=font) for t in texts]
      printer.print_multi(labels)

Getting More Help
-----------------

If you can't solve your issue:

1. **Check GitHub Issues**

   * Search existing issues: https://github.com/nbuchwitz/ptouch/issues
   * Someone may have had the same problem

2. **Enable Debug Logging**

   .. code-block:: python

      import logging

      logging.basicConfig(level=logging.DEBUG)
      # Now run your code - more verbose output

3. **Create Minimal Example**

   * Simplify your code to smallest example that reproduces the issue
   * Remove unrelated code
   * Use simple test data

4. **File a Bug Report**

   Include:

   * Python version: ``python --version``
   * Package version: ``pip show ptouch``
   * Operating system
   * Printer model
   * Minimal code example
   * Complete error message with stack trace
   * What you've already tried

   Create issue at: https://github.com/nbuchwitz/ptouch/issues/new

5. **Check Documentation**

   * :doc:`quickstart` - Basic usage
   * :doc:`userguide` - Common patterns
   * :doc:`advanced` - Performance optimization
   * :doc:`api/printer` - API reference
