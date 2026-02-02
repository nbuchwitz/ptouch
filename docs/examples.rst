Examples
========

This page provides practical, real-world examples you can adapt for your projects.

Asset Management Labels
-----------------------

Create sequential asset tags:

.. code-block:: python

   from ptouch import ConnectionNetwork, PTP900, TextLabel, LaminatedTape12mm
   from PIL import ImageFont

   connection = ConnectionNetwork("192.168.1.100")
   printer = PTP900(connection)
   font = ImageFont.truetype("/path/to/font.ttf", 36)

   # Generate 100 asset tags
   labels = []
   for i in range(1, 101):
       label = TextLabel(
           f"ASSET-{i:04d}",
           LaminatedTape12mm,
           font=font,
           align=TextLabel.Align.CENTER
       )
       labels.append(label)

   # Print efficiently with half-cuts
   printer.print_multi(labels)

Cable Labels
------------

Create matching pairs for cable ends:

.. code-block:: python

   from ptouch import ConnectionUSB, PTE550W, TextLabel, LaminatedTape9mm
   from PIL import ImageFont

   connection = ConnectionUSB()
   printer = PTE550W(connection)
   font = ImageFont.load_default()

   cables = [
       ("Server 1", "Switch Port 24"),
       ("Server 2", "Switch Port 25"),
       ("Router", "Firewall WAN"),
   ]

   for cable_a, cable_b in cables:
       # Print both ends
       label_a = TextLabel(cable_a, LaminatedTape9mm, font=font)
       label_b = TextLabel(cable_b, LaminatedTape9mm, font=font)
       printer.print_multi([label_a, label_b])

Server Rack Labels
------------------

Create detailed server identification labels:

.. code-block:: python

   from PIL import Image, ImageDraw, ImageFont

   def create_server_label(hostname, ip, location, dpi=360):
       # Calculate dimensions for 36mm tape at 360 DPI
       height = int(32 * dpi / 25.4)  # ~32mm printable area
       width = int(80 * dpi / 25.4)   # 80mm wide label

       img = Image.new("RGB", (width, height), "white")
       draw = ImageDraw.Draw(img)

       # Fonts
       font_large = ImageFont.truetype("/path/to/font.ttf", 48)
       font_small = ImageFont.truetype("/path/to/font.ttf", 24)

       # Draw border
       draw.rectangle([5, 5, width-5, height-5], outline="black", width=3)

       # Draw content
       y = 20
       draw.text((15, y), hostname, font=font_large, fill="black")
       y += 60
       draw.text((15, y), f"IP: {ip}", font=font_small, fill="black")
       y += 35
       draw.text((15, y), f"Rack: {location}", font=font_small, fill="black")

       return img

   # Generate labels
   from ptouch import Label, LaminatedTape36mm

   servers = [
       ("web-prod-01", "10.0.1.10", "R1-U12"),
       ("db-prod-01", "10.0.1.20", "R1-U15"),
       ("app-prod-01", "10.0.1.30", "R1-U18"),
   ]

   labels = []
   for hostname, ip, location in servers:
       img = create_server_label(hostname, ip, location)
       labels.append(Label(img, LaminatedTape36mm))

   printer.print_multi(labels)

QR Code Inventory System
-------------------------

Create QR code labels for inventory tracking:

.. code-block:: python

   import qrcode
   import json
   from PIL import Image, ImageDraw, ImageFont

   def create_inventory_label(item_id, name, location):
       # Create QR code with JSON data
       data = json.dumps({
           "id": item_id,
           "name": name,
           "location": location
       })

       qr = qrcode.QRCode(
           version=1,
           error_correction=qrcode.constants.ERROR_CORRECT_M,
           box_size=4,
           border=1
       )
       qr.add_data(data)
       qr.make(fit=True)
       qr_img = qr.make_image(fill_color="black", back_color="white")

       # Create composite image with QR + text
       qr_size = qr_img.size[0]
       text_width = 300
       width = qr_size + text_width + 20
       height = qr_size

       img = Image.new("RGB", (width, height), "white")
       img.paste(qr_img, (10, 0))

       # Add text
       draw = ImageDraw.Draw(img)
       font_name = ImageFont.truetype("/path/to/font.ttf", 28)
       font_id = ImageFont.truetype("/path/to/font.ttf", 20)

       text_x = qr_size + 20
       draw.text((text_x, 20), name, font=font_name, fill="black")
       draw.text((text_x, 55), f"ID: {item_id}", font=font_id, fill="black")
       draw.text((text_x, 85), location, font=font_id, fill="black")

       return img

   # Create inventory labels
   items = [
       ("INV001", "Laptop Dell XPS", "Shelf A3"),
       ("INV002", "Monitor LG 27\"", "Shelf A4"),
       ("INV003", "Keyboard Mech", "Shelf B1"),
   ]

   labels = []
   for item_id, name, location in items:
       img = create_inventory_label(item_id, name, location)
       labels.append(Label(img, LaminatedTape36mm))

   printer.print_multi(labels)

Warning and Safety Labels
--------------------------

Create attention-grabbing warning labels:

.. code-block:: python

   from PIL import Image, ImageDraw, ImageFont

   def create_warning_label(text, dpi=360):
       height = int(32 * dpi / 25.4)
       width = int(100 * dpi / 25.4)

       img = Image.new("RGB", (width, height), "white")
       draw = ImageDraw.Draw(img)

       # Yellow/black warning stripe border
       stripe_width = 20
       for i in range(0, width, stripe_width * 2):
           # Top border
           draw.rectangle([i, 0, i+stripe_width, 15], fill="yellow")
           draw.rectangle([i+stripe_width, 0, i+stripe_width*2, 15], fill="black")
           # Bottom border
           draw.rectangle([i, height-15, i+stripe_width, height], fill="yellow")
           draw.rectangle([i+stripe_width, height-15, i+stripe_width*2, height], fill="black")

       # Text
       font = ImageFont.truetype("/path/to/font-bold.ttf", 48)
       bbox = draw.textbbox((0, 0), text, font=font)
       text_width = bbox[2] - bbox[0]
       text_height = bbox[3] - bbox[1]

       x = (width - text_width) // 2
       y = (height - text_height) // 2

       # Add shadow for emphasis
       draw.text((x+2, y+2), text, font=font, fill="gray")
       draw.text((x, y), text, font=font, fill="red")

       return img

   warnings = ["CAUTION", "HIGH VOLTAGE", "DO NOT TOUCH"]
   labels = [Label(create_warning_label(w), LaminatedTape36mm) for w in warnings]
   printer.print_multi(labels)

Batch Processing from CSV
--------------------------

Read label data from CSV file:

.. code-block:: python

   import csv
   from ptouch import TextLabel, LaminatedTape12mm

   def process_csv_labels(csv_file, printer):
       labels = []

       with open(csv_file, 'r') as f:
           reader = csv.DictReader(f)
           for row in reader:
               # Assuming CSV has 'text' and 'width' columns
               text = row['text']
               width_mm = float(row.get('width', 0)) or None

               label = TextLabel(
                   text,
                   LaminatedTape12mm,
                   font=ImageFont.load_default(),
                   width_mm=width_mm
               )
               labels.append(label)

       print(f"Printing {len(labels)} labels...")
       printer.print_multi(labels)
       print("Complete")

   # Usage
   process_csv_labels("labels.csv", printer)

Example CSV (labels.csv):

.. code-block:: text

   text,width
   "Server A",40
   "Server B",40
   "Router",30
   "Switch",30

Configuration File Labels
--------------------------

Generate labels for device configurations:

.. code-block:: python

   import yaml
   from ptouch import TextLabel, Label, LaminatedTape18mm
   from PIL import Image, ImageDraw, ImageFont

   def load_device_config(yaml_file):
       with open(yaml_file) as f:
           return yaml.safe_load(f)

   def create_device_label(device_info):
       # Create multi-line label
       lines = [
           device_info['name'],
           f"IP: {device_info['ip']}",
           f"MAC: {device_info['mac']}",
       ]

       # Calculate dimensions
       font = ImageFont.truetype("/path/to/font.ttf", 24)
       line_height = 35
       height = int(18 * 360 / 25.4)  # 18mm tape
       width = 400

       img = Image.new("RGB", (width, height), "white")
       draw = ImageDraw.Draw(img)

       y = 10
       for line in lines:
           draw.text((10, y), line, font=font, fill="black")
           y += line_height

       return Label(img, LaminatedTape18mm)

   # Load and print
   config = load_device_config("devices.yaml")
   labels = [create_device_label(dev) for dev in config['devices']]
   printer.print_multi(labels)

Example YAML (devices.yaml):

.. code-block:: yaml

   devices:
     - name: "Office Router"
       ip: "192.168.1.1"
       mac: "00:11:22:33:44:55"
     - name: "NAS Server"
       ip: "192.168.1.100"
       mac: "00:11:22:33:44:66"

Barcode Labels
--------------

Create Code39 barcodes (using python-barcode library):

.. code-block:: python

   import barcode
   from barcode.writer import ImageWriter
   from io import BytesIO

   def create_barcode_label(code):
       # Generate barcode
       code39 = barcode.get('code39', code, writer=ImageWriter())

       # Render to image
       buffer = BytesIO()
       code39.write(buffer, options={
           'module_height': 10.0,
           'module_width': 0.3,
           'text_distance': 3.0,
           'font_size': 12,
       })

       buffer.seek(0)
       img = Image.open(buffer)

       return Label(img.convert("RGB"), LaminatedTape12mm)

   # Generate barcode labels
   codes = ["ABC123", "DEF456", "GHI789"]
   labels = [create_barcode_label(code) for code in codes]
   printer.print_multi(labels)

Interactive Label Maker
-----------------------

Simple interactive CLI for making labels:

.. code-block:: python

   def interactive_label_maker(printer):
       print("Interactive Label Maker")
       print("=" * 40)

       while True:
           text = input("\\nEnter label text (or 'quit'): ").strip()
           if text.lower() == 'quit':
               break

           tape_width = input("Tape width (6/9/12/18/24/36mm) [12]: ").strip()
           tape_width = int(tape_width) if tape_width else 12

           tape_map = {
               6: LaminatedTape6mm,
               9: LaminatedTape9mm,
               12: LaminatedTape12mm,
               18: LaminatedTape18mm,
               24: LaminatedTape24mm,
               36: LaminatedTape36mm,
           }

           tape = tape_map.get(tape_width, LaminatedTape12mm)

           label = TextLabel(
               text,
               tape,
               font=ImageFont.load_default(),
               align=TextLabel.Align.CENTER
           )

           try:
               printer.print(label)
               print("Label printed!")
           except Exception as e:
               print(f"Error: {e}")

   # Usage
   interactive_label_maker(printer)

More Examples
-------------

For more examples, check out:

* :doc:`advanced` - Advanced techniques and optimizations
* :doc:`troubleshooting` - Solutions to common problems
