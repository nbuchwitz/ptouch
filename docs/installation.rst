Installation
============

Basic Installation
------------------

Install from PyPI using pip:

.. code-block:: bash

   pip install ptouch

This installs the core library with network connection support.

With USB Support
----------------

For USB connection support, install with the ``usb`` extra:

.. code-block:: bash

   pip install ptouch[usb]

This adds the ``pyusb`` dependency required for USB communication.

USB Permissions (Linux)
~~~~~~~~~~~~~~~~~~~~~~~~

On Linux, USB access requires proper permissions. You have two options:

**Option 1: Create udev rule (Recommended)**

Create ``/etc/udev/rules.d/99-brother-ptouch.rules``:

.. code-block:: text

   # Brother PT-E550W
   SUBSYSTEM=="usb", ATTR{idVendor}=="04f9", ATTR{idProduct}=="2060", MODE="0666"

   # Brother PT-P750W
   SUBSYSTEM=="usb", ATTR{idVendor}=="04f9", ATTR{idProduct}=="2062", MODE="0666"

   # Brother PT-P900/P900W/P910BT/P950NW
   SUBSYSTEM=="usb", ATTR{idVendor}=="04f9", ATTR{idProduct}=="20af", MODE="0666"

Then reload udev rules:

.. code-block:: bash

   sudo udevadm control --reload-rules
   sudo udevadm trigger

**Option 2: Run with sudo**

.. code-block:: bash

   sudo python your_script.py

Development Installation
-------------------------

For development, clone the repository and install in editable mode:

.. code-block:: bash

   git clone https://github.com/nbuchwitz/ptouch.git
   cd ptouch
   pip install -e ".[dev,test,usb]"

This installs the package with all optional dependencies:

* ``dev`` - Linting and type checking tools (ruff, mypy)
* ``test`` - Testing framework (pytest, pytest-cov)
* ``usb`` - USB support (pyusb)

Requirements
------------

* Python 3.11 or later
* Pillow (image processing)
* packbits (TIFF compression)
* pyusb (optional, for USB support)

Verifying Installation
-----------------------

Test your installation:

.. code-block:: python

   import ptouch
   print(ptouch.__version__)

   # Check available printers
   from ptouch import PTE550W, PTP750W, PTP900
   print("Available printers:", [PTE550W, PTP750W, PTP900])

Next Steps
----------

Continue to the :doc:`quickstart` guide to print your first label.
