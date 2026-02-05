# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for the ptouch.tape module."""

import pytest

from ptouch.tape import (
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


class TestTapeWidths:
    """Test tape width attributes."""

    @pytest.mark.parametrize(
        "tape_class,expected_width",
        [
            (Tape3_5mm, 4),
            (Tape6mm, 6),
            (Tape9mm, 9),
            (Tape12mm, 12),
            (Tape18mm, 18),
            (Tape24mm, 24),
            (Tape36mm, 36),
        ],
    )
    def test_tape_width(self, tape_class: type[Tape], expected_width: int) -> None:
        """Test that tape classes have correct width_mm."""
        tape = tape_class()
        assert tape.width_mm == expected_width

    @pytest.mark.parametrize(
        "tape_class,expected_width",
        [
            (Tape3_5mm, 4),
            (Tape6mm, 6),
            (Tape9mm, 9),
            (Tape12mm, 12),
            (Tape18mm, 18),
            (Tape24mm, 24),
            (Tape36mm, 36),
        ],
    )
    def test_tape_width_class_attribute(self, tape_class: type[Tape], expected_width: int) -> None:
        """Test that width_mm is accessible as class attribute."""
        assert tape_class.width_mm == expected_width


class TestTapeInheritance:
    """Test tape class inheritance."""

    def test_heat_shrink_tube_inherits_from_tape(self) -> None:
        """Test that HeatShrinkTube inherits from Tape."""
        assert issubclass(HeatShrinkTube, Tape)

    @pytest.mark.parametrize(
        "tape_class",
        [
            Tape3_5mm,
            Tape6mm,
            Tape9mm,
            Tape12mm,
            Tape18mm,
            Tape24mm,
            Tape36mm,
        ],
    )
    def test_tape_sizes_inherit_from_tape(self, tape_class: type[Tape]) -> None:
        """Test that all tape sizes inherit from Tape."""
        assert issubclass(tape_class, Tape)


class TestTapeInstantiation:
    """Test tape instantiation."""

    @pytest.mark.parametrize(
        "tape_class",
        [
            Tape3_5mm,
            Tape6mm,
            Tape9mm,
            Tape12mm,
            Tape18mm,
            Tape24mm,
            Tape36mm,
        ],
    )
    def test_tape_can_be_instantiated(self, tape_class: type[Tape]) -> None:
        """Test that tape classes can be instantiated."""
        tape = tape_class()
        assert isinstance(tape, tape_class)
        assert isinstance(tape, Tape)


class TestDeprecatedAliases:
    """Test deprecated LaminatedTape* aliases."""

    @pytest.mark.parametrize(
        "deprecated_class,new_class,expected_width",
        [
            (LaminatedTape3_5mm, Tape3_5mm, 4),
            (LaminatedTape6mm, Tape6mm, 6),
            (LaminatedTape9mm, Tape9mm, 9),
            (LaminatedTape12mm, Tape12mm, 12),
            (LaminatedTape18mm, Tape18mm, 18),
            (LaminatedTape24mm, Tape24mm, 24),
            (LaminatedTape36mm, Tape36mm, 36),
        ],
    )
    def test_deprecated_alias_emits_warning(
        self, deprecated_class: type, new_class: type, expected_width: int
    ) -> None:
        """Test that deprecated aliases emit DeprecationWarning."""
        with pytest.warns(DeprecationWarning, match="deprecated"):
            tape = deprecated_class()
        assert tape.width_mm == expected_width
        assert isinstance(tape, new_class)
        assert isinstance(tape, Tape)

    def test_laminated_tape_base_emits_warning(self) -> None:
        """Test that LaminatedTape base class emits DeprecationWarning."""
        with pytest.warns(DeprecationWarning, match="LaminatedTape is deprecated"):
            LaminatedTape()

    @pytest.mark.parametrize(
        "deprecated_class,new_class",
        [
            (LaminatedTape3_5mm, Tape3_5mm),
            (LaminatedTape6mm, Tape6mm),
            (LaminatedTape9mm, Tape9mm),
            (LaminatedTape12mm, Tape12mm),
            (LaminatedTape18mm, Tape18mm),
            (LaminatedTape24mm, Tape24mm),
            (LaminatedTape36mm, Tape36mm),
        ],
    )
    def test_deprecated_alias_is_subclass_of_new_class(
        self, deprecated_class: type, new_class: type
    ) -> None:
        """Test that deprecated aliases are subclasses of their new counterparts."""
        assert issubclass(deprecated_class, new_class)
        assert issubclass(deprecated_class, Tape)


class TestHeatShrinkTubeWidths:
    """Test heat shrink tube width attributes."""

    @pytest.mark.parametrize(
        "tube_class,expected_width",
        [
            # 2:1 series
            (HeatShrinkTube5_8mm, 6),
            (HeatShrinkTube8_8mm, 9),
            (HeatShrinkTube11_7mm, 12),
            (HeatShrinkTube17_7mm, 18),
            (HeatShrinkTube23_6mm, 24),
            # 3:1 series
            (HeatShrinkTube3_1_5_2mm, 5),
            (HeatShrinkTube3_1_9_0mm, 9),
            (HeatShrinkTube3_1_11_2mm, 11),
            (HeatShrinkTube3_1_21_0mm, 21),
            (HeatShrinkTube3_1_31_0mm, 31),
        ],
    )
    def test_heat_shrink_tube_width(
        self, tube_class: type[HeatShrinkTube], expected_width: int
    ) -> None:
        """Test that heat shrink tube classes have correct width_mm."""
        tube = tube_class()
        assert tube.width_mm == expected_width

    @pytest.mark.parametrize(
        "tube_class,expected_width",
        [
            # 2:1 series
            (HeatShrinkTube5_8mm, 6),
            (HeatShrinkTube8_8mm, 9),
            (HeatShrinkTube11_7mm, 12),
            (HeatShrinkTube17_7mm, 18),
            (HeatShrinkTube23_6mm, 24),
            # 3:1 series
            (HeatShrinkTube3_1_5_2mm, 5),
            (HeatShrinkTube3_1_9_0mm, 9),
            (HeatShrinkTube3_1_11_2mm, 11),
            (HeatShrinkTube3_1_21_0mm, 21),
            (HeatShrinkTube3_1_31_0mm, 31),
        ],
    )
    def test_heat_shrink_tube_width_class_attribute(
        self, tube_class: type[HeatShrinkTube], expected_width: int
    ) -> None:
        """Test that width_mm is accessible as class attribute."""
        assert tube_class.width_mm == expected_width


class TestHeatShrinkTubeInheritance:
    """Test heat shrink tube class inheritance."""

    @pytest.mark.parametrize(
        "tube_class",
        [
            # 2:1 series
            HeatShrinkTube5_8mm,
            HeatShrinkTube8_8mm,
            HeatShrinkTube11_7mm,
            HeatShrinkTube17_7mm,
            HeatShrinkTube23_6mm,
            # 3:1 series
            HeatShrinkTube3_1_5_2mm,
            HeatShrinkTube3_1_9_0mm,
            HeatShrinkTube3_1_11_2mm,
            HeatShrinkTube3_1_21_0mm,
            HeatShrinkTube3_1_31_0mm,
        ],
    )
    def test_heat_shrink_tube_inherits_from_heat_shrink_tube_base(
        self, tube_class: type[HeatShrinkTube]
    ) -> None:
        """Test that all heat shrink tube sizes inherit from HeatShrinkTube."""
        assert issubclass(tube_class, HeatShrinkTube)
        assert issubclass(tube_class, Tape)


class TestHeatShrinkTubeInstantiation:
    """Test heat shrink tube instantiation."""

    @pytest.mark.parametrize(
        "tube_class",
        [
            # 2:1 series
            HeatShrinkTube5_8mm,
            HeatShrinkTube8_8mm,
            HeatShrinkTube11_7mm,
            HeatShrinkTube17_7mm,
            HeatShrinkTube23_6mm,
            # 3:1 series
            HeatShrinkTube3_1_5_2mm,
            HeatShrinkTube3_1_9_0mm,
            HeatShrinkTube3_1_11_2mm,
            HeatShrinkTube3_1_21_0mm,
            HeatShrinkTube3_1_31_0mm,
        ],
    )
    def test_heat_shrink_tube_can_be_instantiated(self, tube_class: type[HeatShrinkTube]) -> None:
        """Test that heat shrink tube classes can be instantiated."""
        tube = tube_class()
        assert isinstance(tube, tube_class)
        assert isinstance(tube, HeatShrinkTube)
        assert isinstance(tube, Tape)
