# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tape types for Brother P-touch label printers."""

import warnings
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


class Tape3_5mm(Tape):
    """3.5mm tape.

    Note: Media size reported by printer is 4mm.
    """

    width_mm = 4


class Tape6mm(Tape):
    """6mm tape."""

    width_mm = 6


class Tape9mm(Tape):
    """9mm tape."""

    width_mm = 9


class Tape12mm(Tape):
    """12mm tape."""

    width_mm = 12


class Tape18mm(Tape):
    """18mm tape."""

    width_mm = 18


class Tape24mm(Tape):
    """24mm tape."""

    width_mm = 24


class Tape36mm(Tape):
    """36mm tape."""

    width_mm = 36


class HeatShrinkTape(Tape):
    """Base class for heat shrink tube tapes (HSe series).

    Heat shrink tubes shrink when heated to wrap around cables and wires.
    They have different printable area constraints than laminated tapes.
    """

    pass


# =============================================================================
# Deprecated aliases for backward compatibility
# =============================================================================


def _deprecated_alias(new_class: type, old_name: str) -> type:
    """Create a deprecated alias class that warns on instantiation."""

    class DeprecatedTape(new_class):
        def __init__(self) -> None:
            warnings.warn(
                f"{old_name} is deprecated, use {new_class.__name__} instead",
                DeprecationWarning,
                stacklevel=2,
            )
            super().__init__()

    DeprecatedTape.__name__ = old_name
    DeprecatedTape.__qualname__ = old_name
    DeprecatedTape.__doc__ = f"Deprecated: Use {new_class.__name__} instead."
    return DeprecatedTape


# Deprecated base class alias
class LaminatedTape(Tape):
    """Deprecated: Use Tape instead.

    .. deprecated::
        The LaminatedTape class is deprecated. Use Tape directly.
    """

    def __init__(self) -> None:
        warnings.warn(
            "LaminatedTape is deprecated, use Tape instead",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()


# Deprecated tape size aliases
LaminatedTape3_5mm = _deprecated_alias(Tape3_5mm, "LaminatedTape3_5mm")
LaminatedTape6mm = _deprecated_alias(Tape6mm, "LaminatedTape6mm")
LaminatedTape9mm = _deprecated_alias(Tape9mm, "LaminatedTape9mm")
LaminatedTape12mm = _deprecated_alias(Tape12mm, "LaminatedTape12mm")
LaminatedTape18mm = _deprecated_alias(Tape18mm, "LaminatedTape18mm")
LaminatedTape24mm = _deprecated_alias(Tape24mm, "LaminatedTape24mm")
LaminatedTape36mm = _deprecated_alias(Tape36mm, "LaminatedTape36mm")
