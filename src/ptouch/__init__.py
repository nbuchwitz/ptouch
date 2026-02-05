# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Brother P-touch label printer driver.

This module provides a Python interface for Brother P-touch label printers,
supporting both USB and network connections. It handles raster image generation,
compression, and printer-specific command sequences.

Supported printers:
    - PT-E550W (128 pins, 180 DPI)
    - PT-P750W (128 pins, 180 DPI)
    - PT-P900 (560 pins, 360 DPI)
    - PT-P900W (560 pins, 360 DPI)
    - PT-P910BT (560 pins, 360 DPI)
    - PT-P950NW (560 pins, 360 DPI)

Example usage:
    >>> from ptouch import PTP900W, ConnectionNetwork, Tape36mm, TextLabel
    >>> conn = ConnectionNetwork("192.168.1.100")
    >>> printer = PTP900W(conn)
    >>> label = TextLabel("Hello, World!", Tape36mm)
    >>> printer.print(label)
"""

from .connection import (
    Connection,
    ConnectionNetwork,
    ConnectionUSB,
    PrinterConnectionError,
    PrinterNetworkError,
    PrinterNotFoundError,
    PrinterPermissionError,
    PrinterTimeoutError,
    PrinterWriteError,
    parse_usb_uri,
)
from .label import Align, Label, TextLabel
from .printer import LabelPrinter, MediaType, TapeConfig
from .printers import PTE550W, PTP750W, PTP900, PTP900W, PTP910BT, PTP950NW
from .tape import (
    # Heat shrink tubes (HSe series)
    HeatShrinkTube,
    HeatShrinkTube3_1_5_2mm,
    HeatShrinkTube3_1_9_0mm,
    HeatShrinkTube3_1_11_2mm,
    HeatShrinkTube3_1_21_0mm,
    HeatShrinkTube3_1_31_0mm,
    HeatShrinkTube5_8mm,
    HeatShrinkTube8_8mm,
    HeatShrinkTube11_7mm,
    HeatShrinkTube17_7mm,
    HeatShrinkTube23_6mm,
    # Deprecated aliases (use Tape*mm instead)
    LaminatedTape,
    LaminatedTape3_5mm,
    LaminatedTape6mm,
    LaminatedTape9mm,
    LaminatedTape12mm,
    LaminatedTape18mm,
    LaminatedTape24mm,
    LaminatedTape36mm,
    Tape,
    Tape3_5mm,
    Tape6mm,
    Tape9mm,
    Tape12mm,
    Tape18mm,
    Tape24mm,
    Tape36mm,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Enums
    "MediaType",
    "Align",
    # Config
    "TapeConfig",
    # Connections
    "Connection",
    "ConnectionUSB",
    "ConnectionNetwork",
    "PrinterConnectionError",
    "PrinterNetworkError",
    "PrinterNotFoundError",
    "PrinterPermissionError",
    "PrinterTimeoutError",
    "PrinterWriteError",
    "parse_usb_uri",
    # Printers
    "LabelPrinter",
    "PTE550W",
    "PTP750W",
    "PTP900",
    "PTP900W",
    "PTP910BT",
    "PTP950NW",
    # Tapes
    "Tape",
    "Tape3_5mm",
    "Tape6mm",
    "Tape9mm",
    "Tape12mm",
    "Tape18mm",
    "Tape24mm",
    "Tape36mm",
    # Heat shrink tubes (HSe series)
    "HeatShrinkTube",
    "HeatShrinkTube5_8mm",
    "HeatShrinkTube8_8mm",
    "HeatShrinkTube11_7mm",
    "HeatShrinkTube17_7mm",
    "HeatShrinkTube23_6mm",
    "HeatShrinkTube3_1_5_2mm",
    "HeatShrinkTube3_1_9_0mm",
    "HeatShrinkTube3_1_11_2mm",
    "HeatShrinkTube3_1_21_0mm",
    "HeatShrinkTube3_1_31_0mm",
    # Deprecated tape aliases (use Tape*mm instead)
    "LaminatedTape",
    "LaminatedTape3_5mm",
    "LaminatedTape6mm",
    "LaminatedTape9mm",
    "LaminatedTape12mm",
    "LaminatedTape18mm",
    "LaminatedTape24mm",
    "LaminatedTape36mm",
    # Labels
    "Label",
    "TextLabel",
]
