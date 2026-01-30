# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Configuration classes and constants for Brother P-touch printers."""

from dataclasses import dataclass


@dataclass
class TapeConfig:
    """Pin configuration for a specific printer/tape combination.

    Attributes
    ----------
    left_pins : int
        Number of unused pins on the left margin.
    print_pins : int
        Number of pins in the printable area.
    right_pins : int
        Number of unused pins on the right margin.
    """

    left_pins: int
    print_pins: int
    right_pins: int


# USB vendor and product identifiers
USB_VENDOR_ID = 0x04F9
USB_PRODUCT_ID_PT_E550W = 0x2060
USB_PRODUCT_ID_PT_P900W = 0x2085
