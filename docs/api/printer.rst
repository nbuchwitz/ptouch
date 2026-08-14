Printer Module
==============

The printer module provides the base printer class and printer implementations for specific Brother P-touch models.

Base Printer Class
------------------

.. automodule:: ptouch.printer
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Printer Implementations
-----------------------

.. automodule:: ptouch.printers
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Supported Printers
------------------

PT-D600
~~~~~~~

* **Class**: ``PTD600``
* **Resolution**: 180x180 DPI
* **Print head**: 128 pins
* **Max tape width**: 24mm
* **Features**: Auto-cut, Half-cut, Mirror print
* **Protocol note**: Uses the legacy ``ESC i R 01`` raster-start command and
  a 100-byte initialization sequence.
* **High-resolution note**: Hardware experiments found evidence of 180x360 DPI
  half-step feed, but this support intentionally exposes only 180x180 DPI.
  The generic renderer cannot yet provide additional source detail; renderer
  work and unsupported-option policy are deferred for separate review.
* **Tape note**: Laminated TZe tape widths are supported. Heat-shrink
  geometry remains unverified.

PT-E550W Series
~~~~~~~~~~~~~~~

* **Class**: ``PTE550W``
* **Resolution**: 180 DPI (standard), 360 DPI (high)
* **Print head**: 128 pins
* **Max tape width**: 24mm
* **Features**: Auto-cut, Half-cut

PT-P750W Series
~~~~~~~~~~~~~~~

* **Class**: ``PTP750W``
* **Resolution**: 180 DPI (standard), 360 DPI (high)
* **Print head**: 128 pins
* **Max tape width**: 24mm
* **Features**: Auto-cut, Half-cut

PT-P900 Series
~~~~~~~~~~~~~~

All P900 series printers share the same specifications:

* **Classes**: ``PTP900``, ``PTP900W``, ``PTP910BT``, ``PTP950NW``
* **Resolution**: 360 DPI (standard), 720 DPI (high)
* **Print head**: 560 pins
* **Max tape width**: 36mm
* **Features**: Auto-cut, Half-cut, Page number cuts

See Also
--------

* :doc:`../quickstart` - Basic printing examples
* :doc:`../userguide` - Multi-label printing and print settings
* :doc:`../advanced` - High-resolution mode and optimization
