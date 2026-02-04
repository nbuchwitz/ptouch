Label Module
============

The label module provides classes for creating text and image labels.

.. automodule:: ptouch.label
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Label Types
-----------

Label
~~~~~

Base class for image-based labels. Use this when you have a pre-rendered image.

**Key attributes:**

* ``image`` - PIL Image object
* ``tape`` - Tape type (e.g., ``Tape36mm``)

TextLabel
~~~~~~~~~

Specialized label class for text rendering with automatic sizing and alignment.

**Key attributes:**

* ``text`` - Text to print
* ``tape`` - Tape type
* ``font`` - ImageFont object or path to TTF file
* ``align`` - Alignment flags (e.g., ``TextLabel.Align.CENTER``)
* ``auto_size`` - Whether to auto-size font to tape height (default: True)
* ``width_mm`` - Fixed label width in mm (default: None for auto-width)

Alignment Options
-----------------

Text alignment can be combined using the ``|`` operator:

Horizontal Alignment
~~~~~~~~~~~~~~~~~~~~

* ``Align.LEFT`` - Align text to left edge
* ``Align.HCENTER`` - Center text horizontally
* ``Align.RIGHT`` - Align text to right edge

Vertical Alignment
~~~~~~~~~~~~~~~~~~

* ``Align.TOP`` - Align text to top edge
* ``Align.VCENTER`` - Center text vertically
* ``Align.BOTTOM`` - Align text to bottom edge

Combined Alignment
~~~~~~~~~~~~~~~~~~

* ``Align.CENTER`` - Center both horizontally and vertically (``HCENTER | VCENTER``)

Example Usage
-------------

Image Label
~~~~~~~~~~~

.. code-block:: python

   from PIL import Image
   from ptouch import Label, Tape36mm

   image = Image.open("logo.png")
   label = Label(image, Tape36mm)
   printer.print(label)

Text Label with Auto-Sizing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ptouch import TextLabel, Tape36mm
   from PIL import ImageFont

   font = ImageFont.load_default()
   label = TextLabel(
       "Hello World",
       Tape36mm,
       font=font,
       align=TextLabel.Align.CENTER
   )

Text Label with Fixed Size
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   font = ImageFont.truetype("/path/to/font.ttf", 48)
   label = TextLabel(
       "Fixed Size",
       Tape36mm,
       font=font,
       auto_size=False,  # Use font's built-in size
       align=TextLabel.Align.LEFT | TextLabel.Align.TOP
   )

Text Label with Fixed Width
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   label = TextLabel(
       "Short",
       Tape36mm,
       font=font,
       width_mm=50.0  # Create 50mm wide label
   )

Custom Alignment
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Top-left alignment
   label = TextLabel(
       "Top Left",
       Tape36mm,
       font=font,
       align=TextLabel.Align.LEFT | TextLabel.Align.TOP
   )

   # Bottom-right alignment
   label = TextLabel(
       "Bottom Right",
       Tape36mm,
       font=font,
       align=TextLabel.Align.RIGHT | TextLabel.Align.BOTTOM
   )

   # Centered (shorthand)
   label = TextLabel(
       "Centered",
       Tape36mm,
       font=font,
       align=TextLabel.Align.CENTER
   )
