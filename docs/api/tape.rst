Tape Module
===========

The tape module provides tape type definitions for Brother P-touch label printers.

.. automodule:: ptouch.tape
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Supported Tapes
---------------

TZe Series Tapes
~~~~~~~~~~~~~~~~

TZe tapes are the most common tape type for Brother P-touch printers.

Available Widths
^^^^^^^^^^^^^^^^

* ``Tape3_5mm`` - 3.5mm tape
* ``Tape6mm`` - 6mm tape
* ``Tape9mm`` - 9mm tape
* ``Tape12mm`` - 12mm tape
* ``Tape18mm`` - 18mm tape
* ``Tape24mm`` - 24mm tape
* ``Tape36mm`` - 36mm tape (P900 series only)

Compatibility
^^^^^^^^^^^^^

+------------+----------+----------+----------+
| Tape Width | E550W    | P750W    | P900     |
+============+==========+==========+==========+
| 3.5mm      | ✓        | ✓        | ✓        |
+------------+----------+----------+----------+
| 6mm        | ✓        | ✓        | ✓        |
+------------+----------+----------+----------+
| 9mm        | ✓        | ✓        | ✓        |
+------------+----------+----------+----------+
| 12mm       | ✓        | ✓        | ✓        |
+------------+----------+----------+----------+
| 18mm       | ✓        | ✓        | ✓        |
+------------+----------+----------+----------+
| 24mm       | ✓        | ✓        | ✓        |
+------------+----------+----------+----------+
| 36mm       | ✗        | ✗        | ✓        |
+------------+----------+----------+----------+

Tape Configuration
------------------

Each printer model has specific pin configurations for each tape width. The library automatically handles this mapping.

Pin Configuration
~~~~~~~~~~~~~~~~~

For each tape width, the printer needs to know:

* **Left margin pins** - Unused pins on the left
* **Printable area pins** - Pins used for actual printing
* **Right margin pins** - Unused pins on the right

The sum must equal the printer's total pin count (128 for E550W/P750W, 560 for P900 series).

Example: 12mm Tape on PT-E550W
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Left pins: 29
* Printable pins: 70
* Right pins: 29
* Total: 128 (matches printer's TOTAL_PINS)

Example Usage
-------------

Specifying Tape Type
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import TextLabel, Tape36mm
   from PIL import ImageFont

   # Create label with 36mm tape
   font = ImageFont.load_default()
   label = TextLabel("Text", Tape36mm, font=font)

Checking Tape Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import PTE550W, Tape36mm

   printer = PTE550W(connection)

   try:
       config = printer.get_tape_config(Tape36mm)
   except KeyError:
       print("This tape is not compatible with this printer")

Available Tape Widths
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import PTP900

   printer = PTP900(connection)

   # Get all supported tape types
   supported_tapes = printer.PIN_CONFIGS.keys()
   for tape_type in supported_tapes:
       print(f"Supported: {tape_type.__name__} ({tape_type.width_mm}mm)")

Adding Custom Tape Types
-------------------------

See :doc:`../adding_devices` for instructions on adding support for new tape types.

Example:

.. code-block:: python

   from ptouch.tape import Tape

   class Tape48mm(Tape):
       """48mm tape."""
       width_mm = 48

Then add the pin configuration to your printer class:

.. code-block:: python

   from ptouch.printer import TapeConfig

   PIN_CONFIGS = {
       Tape48mm: TapeConfig(
           left_pins=0,
           print_pins=680,
           right_pins=0
       ),
       # ... other tape configs
   }
