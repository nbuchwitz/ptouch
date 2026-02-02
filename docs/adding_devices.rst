Adding Support for New Devices
=================================

This guide explains how to extend the library to support additional Brother P-touch printers and tape types.

Adding a New Printer
---------------------

Step 1: Gather Specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need the following information from the Brother raster command reference:

1. **USB Product ID** - From the printer's USB descriptor
2. **Print head specifications**:

   * Total pins in print head
   * Base resolution (DPI)
   * High resolution (DPI) if supported

3. **Capability flags**:

   * Auto-cut support
   * Half-cut support
   * Page number cuts support

4. **Pin configuration** for each tape width:

   * Left margin pins
   * Printable area pins
   * Right margin pins

Finding USB Product ID
~~~~~~~~~~~~~~~~~~~~~~

Connect the printer and run:

.. code-block:: bash

   # Linux
   lsusb | grep Brother
   # Output: Bus 001 Device 010: ID 04f9:20af Brother Industries, Ltd

   # The product ID is 20af (0x20af in hex)

Or use Python:

.. code-block:: python

   import usb.core

   # Find all Brother devices
   devices = usb.core.find(find_all=True, idVendor=0x04f9)
   for dev in devices:
       print(f"Product ID: {hex(dev.idProduct)}")
       print(f"Product: {dev.product}")

Step 2: Create Printer Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new class in ``src/ptouch/printers.py``:

.. code-block:: python

   from ptouch.printer import LabelPrinter, TapeConfig
   from ptouch.tape import (
       LaminatedTape6mm,
       LaminatedTape9mm,
       LaminatedTape12mm,
       LaminatedTape18mm,
       LaminatedTape24mm,
   )

   class PTP710BT(LabelPrinter):
       """Brother PT-P710BT label printer.

       Specifications:
       - Resolution: 180 DPI (standard), 360 DPI (high)
       - Print head: 128 pins
       - Max tape width: 24mm
       - Supports: Auto-cut, Half-cut
       """

       # USB identification
       USB_PRODUCT_ID = 0x209d  # Replace with actual ID

       # Print head specifications
       TOTAL_PINS = 128
       BYTES_PER_LINE = 16  # TOTAL_PINS / 8
       RESOLUTION_DPI = 180
       RESOLUTION_DPI_HIGH = 360

       # Capability flags
       SUPPORTS_AUTO_CUT = True
       SUPPORTS_HALF_CUT = True
       SUPPORTS_PAGE_NUMBER_CUTS = True

       # Default settings
       DEFAULT_USE_COMPRESSION = True
       DEFAULT_AUTO_CUT = True
       DEFAULT_HALF_CUT = True
       DEFAULT_HIGH_RESOLUTION = False
       DEFAULT_PAGE_NUMBER_CUTS = False

       # Pin configuration for each tape width
       # Values from Brother raster command reference
       PIN_CONFIGS = {
           LaminatedTape6mm: TapeConfig(
               left_pins=48,
               print_pins=32,
               right_pins=48
           ),
           LaminatedTape9mm: TapeConfig(
               left_pins=39,
               print_pins=50,
               right_pins=39
           ),
           LaminatedTape12mm: TapeConfig(
               left_pins=29,
               print_pins=70,
               right_pins=29
           ),
           LaminatedTape18mm: TapeConfig(
               left_pins=8,
               print_pins=112,
               right_pins=8
           ),
           LaminatedTape24mm: TapeConfig(
               left_pins=0,
               print_pins=128,
               right_pins=0
           ),
       }

Step 3: Export the Printer Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add to ``src/ptouch/__init__.py``:

.. code-block:: python

   from .printers import (
       # ... existing imports ...
       PTP710BT,  # Add your new printer
   )

   __all__ = [
       # ... existing exports ...
       "PTP710BT",  # Add to __all__
   ]

Step 4: Add Tests
~~~~~~~~~~~~~~~~~

Create tests in ``tests/test_printers.py``:

.. code-block:: python

   def test_ptp710bt_specifications():
       """Test PTP710BT printer specifications."""
       printer = PTP710BT(mock_connection)

       assert printer.USB_PRODUCT_ID == 0x209d
       assert printer.TOTAL_PINS == 128
       assert printer.RESOLUTION_DPI == 180
       assert printer.RESOLUTION_DPI_HIGH == 360
       assert printer.SUPPORTS_AUTO_CUT is True
       assert printer.SUPPORTS_HALF_CUT is True

   def test_ptp710bt_tape_configs():
       """Test tape configurations for PTP710BT."""
       printer = PTP710BT(mock_connection)

       # Test each tape size
       config = printer.get_tape_config(LaminatedTape12mm)
       assert config.left_pins == 29
       assert config.print_pins == 70
       assert config.right_pins == 29
       assert config.total_pins == 128

   def test_ptp710bt_printing():
       """Test basic printing with PTP710BT."""
       printer = PTP710BT(mock_connection)
       label = Label(sample_image, LaminatedTape12mm)

       printer.print(label)
       assert len(mock_connection.data) > 0

Step 5: Update Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add to the README.md supported printers table and update docs.

Example: P900 Series Printers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The P900 series printers share identical specifications, so they inherit from a common base:

.. code-block:: python

   class PTP900Series(LabelPrinter):
       """Base class for Brother PT-P900 series printers."""

       TOTAL_PINS = 560
       BYTES_PER_LINE = 70
       RESOLUTION_DPI = 360
       RESOLUTION_DPI_HIGH = 720
       # ... rest of common config ...

   class PTP900(PTP900Series):
       """Brother PT-P900 (USB only)."""
       USB_PRODUCT_ID = 0x20af

   class PTP900W(PTP900Series):
       """Brother PT-P900W (USB + WiFi)."""
       USB_PRODUCT_ID = 0x20af  # Same as P900

   class PTP910BT(PTP900Series):
       """Brother PT-P910BT (USB + Bluetooth)."""
       USB_PRODUCT_ID = 0x20af  # Same as P900

   class PTP950NW(PTP900Series):
       """Brother PT-P950NW (USB + WiFi + NFC)."""
       USB_PRODUCT_ID = 0x20af  # Same as P900

Adding a New Tape Type
-----------------------

Step 1: Determine Tape Specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need:

* Physical width in millimeters
* Tape category (laminated, non-laminated, etc.)
* Compatible printers

Step 2: Create Tape Class
~~~~~~~~~~~~~~~~~~~~~~~~~~

Add to ``src/ptouch/tape.py``:

.. code-block:: python

   class LaminatedTape48mm(LaminatedTape):
       """48mm laminated tape (TZe-481, etc.).

       Compatible with larger industrial printers only.
       """
       width_mm = 48

For non-laminated tape:

.. code-block:: python

   class Tape(ABC):
       """Base class for all tape types."""
       width_mm: int

       @property
       @abstractmethod
       def category(self) -> str:
           """Tape category identifier."""
           pass

   class NonLaminatedTape(Tape):
       """Non-laminated (N) series tapes."""

       @property
       def category(self) -> str:
           return "non-laminated"

   class NonLaminatedTape12mm(NonLaminatedTape):
       """12mm non-laminated tape."""
       width_mm = 12

Step 3: Add Pin Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update each compatible printer's ``PIN_CONFIGS``:

.. code-block:: python

   class PTP900(PTP900Series):
       PIN_CONFIGS = {
           # ... existing configs ...
           LaminatedTape48mm: TapeConfig(
               left_pins=0,
               print_pins=680,  # Example - check reference manual
               right_pins=0
           ),
       }

Finding Pin Configuration Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pin configurations come from the Brother raster command reference PDF for your printer model. Look for tables showing:

* Tape width
* Left margin pins
* Effective print area pins
* Right margin pins

The sum must equal ``TOTAL_PINS`` for the printer.

Step 4: Export and Test
~~~~~~~~~~~~~~~~~~~~~~~~

Add to ``src/ptouch/__init__.py``:

.. code-block:: python

   from .tape import (
       # ... existing imports ...
       LaminatedTape48mm,
   )

   __all__ = [
       # ... existing exports ...
       "LaminatedTape48mm",
   ]

Test with your printer:

.. code-block:: python

   def test_new_tape():
       printer = PTP900(mock_connection)
       label = Label(sample_image, LaminatedTape48mm)
       printer.print(label)

Testing Your Changes
--------------------

Unit Tests
~~~~~~~~~~

Run the test suite:

.. code-block:: bash

   pytest tests/

Ensure all existing tests still pass and new tests pass.

Real Hardware Testing
~~~~~~~~~~~~~~~~~~~~~

Test with actual printer:

.. code-block:: python

   from ptouch import ConnectionUSB, PTP710BT, TextLabel, LaminatedTape12mm
   from PIL import ImageFont

   # Test basic functionality
   connection = ConnectionUSB()
   printer = PTP710BT(connection)

   label = TextLabel(
       "Test Label",
       LaminatedTape12mm,
       font=ImageFont.load_default()
   )

   printer.print(label)

Test each tape size supported by the printer.

Contributing Back
-----------------

If you add support for a new device, please consider contributing it back to the project.

See `CONTRIBUTING.md <https://github.com/nbuchwitz/ptouch/blob/main/CONTRIBUTING.md>`_ for detailed guidelines on:

* How to submit pull requests
* Code style and testing requirements
* Documentation standards
* Review process

Common Issues
-------------

Wrong Pin Configuration
~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Labels print with incorrect alignment or clipped edges.

**Solution**: Double-check pin configuration values in the Brother reference manual. Ensure ``left_pins + print_pins + right_pins == TOTAL_PINS``.

USB Product ID Conflicts
~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Wrong printer class is selected.

**Solution**: Many Brother printers share the same USB product ID. The library cannot distinguish between them automatically. Users must select the correct class.

Unsupported Features
~~~~~~~~~~~~~~~~~~~~

**Symptom**: Features work on some printers but not others.

**Solution**: Set capability flags correctly:

.. code-block:: python

   SUPPORTS_AUTO_CUT = False  # If printer doesn't support auto-cut
   SUPPORTS_HALF_CUT = False  # If printer doesn't support half-cut

The library will raise an error if unsupported features are requested.

Resolution Confusion
~~~~~~~~~~~~~~~~~~~~

**Symptom**: High resolution mode doesn't work or produces wrong output.

**Solution**: Check if printer actually supports high resolution:

.. code-block:: python

   RESOLUTION_DPI_HIGH = 0  # Set to 0 if not supported

Resources
---------

* `Brother Developer Portal <https://www.brother.com/>`_ - Raster command reference manuals
* :doc:`api/printer` - API documentation for LabelPrinter class
* :doc:`api/tape` - API documentation for Tape classes
* `GitHub Issues <https://github.com/nbuchwitz/ptouch/issues>`_ - Ask for help

Need Help?
----------

If you're adding support for a device and need assistance:

1. Open a GitHub issue with your printer model
2. Include USB vendor/product ID
3. Link to the printer's raster command reference if available
4. Describe what you've tried

The community can help guide you through the process.
