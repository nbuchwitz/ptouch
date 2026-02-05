# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Concrete printer implementations for Brother P-touch label printers."""

from .printer import LabelPrinter, TapeConfig
from .tape import (
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
    Tape3_5mm,
    Tape6mm,
    Tape9mm,
    Tape12mm,
    Tape18mm,
    Tape24mm,
    Tape36mm,
)


class PTE550W(LabelPrinter):
    """Brother PT-E550W label printer (128 pins, 180 DPI).

    Note: E550W requires compression ON for cutting to work.
    High resolution mode (180x360 dpi) is supported via ESC i K bit 6.
    In high-res mode, each raster line must be sent twice and margin doubled.
    """

    USB_PRODUCT_ID = 0x2060
    TOTAL_PINS = 128
    BYTES_PER_LINE = 16
    RESOLUTION_DPI = 180
    RESOLUTION_DPI_HIGH = 360
    DEFAULT_USE_COMPRESSION = True  # Required for cutting to work

    # Pin configurations from official Brother PT-E550W specification document
    # Source: cv_pte550wp750wp710bt_eng_raster_102.pdf, page 20, section "2.3 Print Area"
    PIN_CONFIGS = {
        # Laminated tapes (TZe series)
        Tape3_5mm: TapeConfig(left_pins=52, print_pins=24, right_pins=52),
        Tape6mm: TapeConfig(left_pins=48, print_pins=32, right_pins=48),
        Tape9mm: TapeConfig(left_pins=39, print_pins=50, right_pins=39),
        Tape12mm: TapeConfig(left_pins=29, print_pins=70, right_pins=29),
        Tape18mm: TapeConfig(left_pins=8, print_pins=112, right_pins=8),
        Tape24mm: TapeConfig(left_pins=0, print_pins=128, right_pins=0),
        # Heat shrink tubes 2:1 series (HSe)
        # Corrected configs: shifted -2 pins (up) based on testing
        HeatShrinkTube5_8mm: TapeConfig(left_pins=52, print_pins=28, right_pins=48),
        HeatShrinkTube8_8mm: TapeConfig(left_pins=42, print_pins=48, right_pins=38),
        HeatShrinkTube11_7mm: TapeConfig(left_pins=33, print_pins=66, right_pins=29),
        HeatShrinkTube17_7mm: TapeConfig(left_pins=13, print_pins=106, right_pins=9),
        HeatShrinkTube23_6mm: TapeConfig(left_pins=0, print_pins=128, right_pins=0),
        # Heat shrink tubes 3:1 series (HSe)
        HeatShrinkTube3_1_5_2mm: TapeConfig(left_pins=56, print_pins=20, right_pins=52),
        HeatShrinkTube3_1_9_0mm: TapeConfig(left_pins=44, print_pins=44, right_pins=40),
        HeatShrinkTube3_1_11_2mm: TapeConfig(left_pins=41, print_pins=50, right_pins=37),
        HeatShrinkTube3_1_21_0mm: TapeConfig(left_pins=6, print_pins=120, right_pins=2),
        # Note: PT-E550W/P750W do NOT support 31.0mm 3:1 tubes
    }


class PTP750W(PTE550W):
    """Brother PT-P750W label printer (128 pins, 180 DPI).

    Inherits all settings from PTE550W.
    """

    USB_PRODUCT_ID = 0x2065


class PTP900Series(LabelPrinter):
    """Base class for Brother PT-P900 series printers (560 pins, 360 DPI).

    This is the base class for all P900 series printers. Use one of the
    specific subclasses (PTP900, PTP900W, PTP950NW, PTP910BT) instead.
    """

    TOTAL_PINS = 560
    BYTES_PER_LINE = 70
    RESOLUTION_DPI = 360
    RESOLUTION_DPI_HIGH = 720
    DEFAULT_USE_COMPRESSION = False

    # Pin configurations from official Brother PT-P900 specification document
    # Source: cv_ptp900_eng_raster_102.pdf, pages 23-24, section 2.3.5 "Raster line"
    PIN_CONFIGS = {
        # Laminated tapes (TZe series)
        Tape3_5mm: TapeConfig(left_pins=248, print_pins=48, right_pins=264),
        Tape6mm: TapeConfig(left_pins=240, print_pins=64, right_pins=256),
        Tape9mm: TapeConfig(left_pins=219, print_pins=106, right_pins=235),
        Tape12mm: TapeConfig(left_pins=197, print_pins=150, right_pins=213),
        Tape18mm: TapeConfig(left_pins=155, print_pins=234, right_pins=171),
        Tape24mm: TapeConfig(left_pins=112, print_pins=320, right_pins=128),
        Tape36mm: TapeConfig(left_pins=45, print_pins=454, right_pins=61),
        # Heat shrink tubes 2:1 series (HSe)
        # Corrected configs: shifted +17 pins down based on Brother software analysis
        HeatShrinkTube5_8mm: TapeConfig(left_pins=261, print_pins=56, right_pins=243),
        HeatShrinkTube8_8mm: TapeConfig(left_pins=241, print_pins=96, right_pins=223),
        HeatShrinkTube11_7mm: TapeConfig(left_pins=223, print_pins=132, right_pins=205),
        HeatShrinkTube17_7mm: TapeConfig(left_pins=183, print_pins=212, right_pins=165),
        HeatShrinkTube23_6mm: TapeConfig(left_pins=161, print_pins=256, right_pins=143),
        # Heat shrink tubes 3:1 series (HSe)
        HeatShrinkTube3_1_5_2mm: TapeConfig(left_pins=269, print_pins=40, right_pins=251),
        HeatShrinkTube3_1_9_0mm: TapeConfig(left_pins=245, print_pins=88, right_pins=227),
        HeatShrinkTube3_1_11_2mm: TapeConfig(left_pins=239, print_pins=100, right_pins=221),
        HeatShrinkTube3_1_21_0mm: TapeConfig(left_pins=169, print_pins=240, right_pins=151),
        HeatShrinkTube3_1_31_0mm: TapeConfig(left_pins=109, print_pins=360, right_pins=91),
    }


class PTP900(PTP900Series):
    """Brother PT-P900 label printer (USB only, no wireless)."""

    USB_PRODUCT_ID = 0x2083


class PTP900W(PTP900Series):
    """Brother PT-P900W label printer (with Wi-Fi)."""

    USB_PRODUCT_ID = 0x2085


class PTP950NW(PTP900Series):
    """Brother PT-P950NW label printer (with network connectivity)."""

    USB_PRODUCT_ID = 0x2086


class PTP910BT(PTP900Series):
    """Brother PT-P910BT label printer (with Bluetooth).

    Note: PT-P910BT does NOT support heat shrink tubes (HSe series).
    """

    USB_PRODUCT_ID = 0x20C7

    # PT-P910BT only supports laminated tapes, not heat shrink tubes
    PIN_CONFIGS = {
        Tape3_5mm: TapeConfig(left_pins=248, print_pins=48, right_pins=264),
        Tape6mm: TapeConfig(left_pins=240, print_pins=64, right_pins=256),
        Tape9mm: TapeConfig(left_pins=219, print_pins=106, right_pins=235),
        Tape12mm: TapeConfig(left_pins=197, print_pins=150, right_pins=213),
        Tape18mm: TapeConfig(left_pins=155, print_pins=234, right_pins=171),
        Tape24mm: TapeConfig(left_pins=112, print_pins=320, right_pins=128),
        Tape36mm: TapeConfig(left_pins=45, print_pins=454, right_pins=61),
    }
