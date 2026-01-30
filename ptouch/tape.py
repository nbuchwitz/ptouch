# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tape types for Brother P-touch label printers."""

from abc import ABC


class Tape(ABC):
    """Abstract base class for P-touch tapes.

    Subclasses must define width_mm as a class attribute.

    Attributes
    ----------
    width_mm : int
        Width of the tape in millimeters (class attribute).
    """

    width_mm: int


class LaminatedTape(Tape):
    """Base class for laminated tapes (TZe series).

    Laminated tapes have a protective layer over the printed content,
    making them durable and resistant to fading, water, and abrasion.
    """

    pass


class LaminatedTape6mm(LaminatedTape):
    """6mm laminated tape."""

    width_mm = 6


class LaminatedTape9mm(LaminatedTape):
    """9mm laminated tape."""

    width_mm = 9


class LaminatedTape12mm(LaminatedTape):
    """12mm laminated tape."""

    width_mm = 12


class LaminatedTape18mm(LaminatedTape):
    """18mm laminated tape."""

    width_mm = 18


class LaminatedTape24mm(LaminatedTape):
    """24mm laminated tape."""

    width_mm = 24


class LaminatedTape36mm(LaminatedTape):
    """36mm laminated tape."""

    width_mm = 36


class HeatShrinkTape(Tape):
    """Base class for heat shrink tube tapes (HSe series).

    Heat shrink tubes shrink when heated to wrap around cables and wires.
    They have different printable area constraints than laminated tapes.
    """

    pass
