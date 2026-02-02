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
