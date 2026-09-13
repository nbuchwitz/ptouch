# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for the ptouch.printer and ptouch.printers modules."""

import pytest
from PIL import Image

from ptouch.label import Label
from ptouch.printer import TapeConfig
from ptouch.printer import MediaType
from ptouch.printers import PTE550W, PTP750W, PTP900, PTP910BT
from ptouch.tape import (
    Tape3_5mm,
    Tape6mm,
    Tape12mm,
    Tape24mm,
    Tape36mm,
)

from .conftest import MockConnection


class TestMediaType:
    """Test MediaType enum."""

    def test_media_type_values(self) -> None:
        """Test that MediaType enum has expected values."""
        assert MediaType.NO_MEDIA.value == 0x00
        assert MediaType.LAMINATED_TAPE.value == 0x01
        assert MediaType.NONLAMINATED_TAPE.value == 0x03
        assert MediaType.HEATSHRINK_TUBE_21.value == 0x11
        assert MediaType.INCOMPATIBLE_TAPE.value == 0xFF


class TestPTE550W:
    """Test PTE550W printer class."""

    def test_class_attributes(self) -> None:
        """Test that class attributes are correctly defined."""
        assert PTE550W.TOTAL_PINS == 128
        assert PTE550W.BYTES_PER_LINE == 16
        assert PTE550W.RESOLUTION_DPI == 180
        assert PTE550W.RESOLUTION_DPI_HIGH == 360
        assert PTE550W.DEFAULT_USE_COMPRESSION is True

    def test_initialization(self, mock_connection: MockConnection) -> None:
        """Test printer initialization."""
        printer = PTE550W(mock_connection)
        assert printer.connection is mock_connection
        assert printer.use_compression is True  # Default
        assert printer.high_resolution is False  # Default

    def test_initialization_with_custom_settings(self, mock_connection: MockConnection) -> None:
        """Test printer initialization with custom settings."""
        printer = PTE550W(mock_connection, use_compression=False, high_resolution=True)
        assert printer.use_compression is False
        assert printer.high_resolution is True

    def test_supports_high_resolution(self, mock_connection: MockConnection) -> None:
        """Test that E550W supports high resolution."""
        printer = PTE550W(mock_connection)
        assert printer.supports_high_resolution is True

    def test_pin_configs(self) -> None:
        """Test that PIN_CONFIGS contains expected tape types."""
        assert Tape3_5mm in PTE550W.PIN_CONFIGS
        assert Tape6mm in PTE550W.PIN_CONFIGS
        assert Tape12mm in PTE550W.PIN_CONFIGS
        assert Tape24mm in PTE550W.PIN_CONFIGS
        # E550W doesn't support 36mm
        assert Tape36mm not in PTE550W.PIN_CONFIGS

    def test_get_tape_config(self, mock_connection: MockConnection) -> None:
        """Test getting tape configuration."""
        printer = PTE550W(mock_connection)
        tape = Tape12mm()
        config = printer.get_tape_config(tape)
        assert isinstance(config, TapeConfig)
        assert config.left_pins == 29
        assert config.print_pins == 70
        assert config.right_pins == 29
        # Total should equal TOTAL_PINS
        assert config.left_pins + config.print_pins + config.right_pins == 128

    def test_get_tape_config_unsupported_tape(self, mock_connection: MockConnection) -> None:
        """Test that unsupported tape raises ValueError."""
        printer = PTE550W(mock_connection)
        tape = Tape36mm()
        with pytest.raises(ValueError, match="not supported"):
            printer.get_tape_config(tape)


class TestSupportedTapes:
    """Test supported_tapes property."""

    def test_supported_tapes_returns_list(self, mock_connection: MockConnection) -> None:
        """Test that supported_tapes returns a list of tape classes."""
        printer = PTE550W(mock_connection)
        tapes = printer.supported_tapes
        assert isinstance(tapes, list)
        assert len(tapes) > 0
        assert Tape6mm in tapes
        assert Tape12mm in tapes
        assert Tape24mm in tapes

    def test_supported_tapes_sorted_by_name(self, mock_connection: MockConnection) -> None:
        """Test that supported_tapes are sorted by class name."""
        printer = PTE550W(mock_connection)
        tapes = printer.supported_tapes
        names = [t.__name__ for t in tapes]
        assert names == sorted(names)

    def test_supported_tapes_excludes_unsupported(self, mock_connection: MockConnection) -> None:
        """Test that E550W doesn't include 36mm tape."""
        printer = PTE550W(mock_connection)
        tapes = printer.supported_tapes
        assert Tape36mm not in tapes

    def test_p900_supports_36mm(self, mock_connection: MockConnection) -> None:
        """Test that P900 includes 36mm tape."""
        printer = PTP900(mock_connection)
        assert Tape36mm in printer.supported_tapes


class TestPTP750W:
    """Test PTP750W printer class."""

    def test_inherits_from_e550w(self) -> None:
        """Test that P750W inherits from E550W."""
        assert issubclass(PTP750W, PTE550W)

    def test_same_attributes_as_e550w(self) -> None:
        """Test that P750W has same attributes as E550W."""
        assert PTP750W.TOTAL_PINS == PTE550W.TOTAL_PINS
        assert PTP750W.PIN_CONFIGS == PTE550W.PIN_CONFIGS


class TestPTP900:
    """Test PTP900 printer class."""

    def test_class_attributes(self) -> None:
        """Test that class attributes are correctly defined."""
        assert PTP900.TOTAL_PINS == 560
        assert PTP900.BYTES_PER_LINE == 70
        assert PTP900.RESOLUTION_DPI == 360
        assert PTP900.RESOLUTION_DPI_HIGH == 720
        assert PTP900.DEFAULT_USE_COMPRESSION is False

    def test_supports_36mm_tape(self) -> None:
        """Test that P900 supports 36mm tape."""
        assert Tape3_5mm in PTP900.PIN_CONFIGS
        assert Tape36mm in PTP900.PIN_CONFIGS

    def test_get_tape_config_36mm(self, mock_connection: MockConnection) -> None:
        """Test getting 36mm tape configuration."""
        printer = PTP900(mock_connection)
        tape = Tape36mm()
        config = printer.get_tape_config(tape)
        assert config.left_pins == 45
        assert config.print_pins == 454
        assert config.right_pins == 61
        assert config.left_pins + config.print_pins + config.right_pins == 560


class TestLabelPrinterCommands:
    """Test LabelPrinter command generation methods."""

    @pytest.fixture
    def printer(self, mock_connection: MockConnection) -> PTE550W:
        """Create a test printer."""
        return PTE550W(mock_connection)

    def test_cmd_invalidate(self, printer: PTE550W) -> None:
        """Test invalidate command generates correct null bytes."""
        cmd = printer._cmd_invalidate(length=100)
        assert len(cmd) == 100
        assert cmd == b"\x00" * 100

    def test_cmd_initialize(self, printer: PTE550W) -> None:
        """Test initialize command (ESC @)."""
        cmd = printer._cmd_initialize()
        assert cmd == b"\x1b\x40"

    def test_cmd_raster_mode(self, printer: PTE550W) -> None:
        """Test raster mode command (ESC i a)."""
        cmd = printer._cmd_raster_mode()
        assert cmd == b"\x1b\x69\x61\x01"

    def test_cmd_mode_settings_auto_cut_on(self, printer: PTE550W) -> None:
        """Test mode settings with auto-cut enabled."""
        cmd = printer._cmd_mode_settings(auto_cut=True, mirror_print=False)
        assert cmd[:3] == b"\x1b\x69\x4d"
        assert cmd[3] & (1 << 6) != 0  # Auto-cut bit set

    def test_cmd_mode_settings_auto_cut_off(self, printer: PTE550W) -> None:
        """Test mode settings with auto-cut disabled."""
        cmd = printer._cmd_mode_settings(auto_cut=False, mirror_print=False)
        assert cmd[:3] == b"\x1b\x69\x4d"
        assert cmd[3] & (1 << 6) == 0  # Auto-cut bit not set

    def test_cmd_advanced_mode_settings_high_res(self, printer: PTE550W) -> None:
        """Test advanced mode settings with high resolution enabled."""
        cmd = printer._cmd_advanced_mode_settings(high_resolution=True)
        assert cmd[:3] == b"\x1b\x69\x4b"
        assert cmd[3] & (1 << 6) != 0  # High-res bit set

    def test_cmd_margin(self, printer: PTE550W) -> None:
        """Test margin command."""
        cmd = printer._cmd_margin(margin=14)
        assert cmd[:3] == b"\x1b\x69\x64"
        # Margin is little-endian 16-bit
        assert cmd[3:5] == b"\x0e\x00"

    def test_cmd_set_compression_on(self, printer: PTE550W) -> None:
        """Test compression command enabled."""
        cmd = printer._cmd_set_compression(tiff_compression=True)
        assert cmd == b"\x4d\x02"

    def test_cmd_set_compression_off(self, printer: PTE550W) -> None:
        """Test compression command disabled."""
        cmd = printer._cmd_set_compression(tiff_compression=False)
        assert cmd == b"\x4d\x00"


class TestLabelPrinterMmToDots:
    """Test mm to dots conversion."""

    def test_mm_to_dots_e550w(self, mock_connection: MockConnection) -> None:
        """Test mm to dots conversion for 180 DPI printer."""
        printer = PTE550W(mock_connection)  # 180 DPI
        # 25.4mm = 1 inch = 180 dots
        assert printer._mm_to_dots(25.4) == 180
        # 2mm margin
        dots = printer._mm_to_dots(2.0)
        assert dots == round(2.0 * 180 / 25.4)  # ~14

    def test_mm_to_dots_p900(self, mock_connection: MockConnection) -> None:
        """Test mm to dots conversion for 360 DPI printer."""
        printer = PTP900(mock_connection)  # 360 DPI
        # 25.4mm = 1 inch = 360 dots
        assert printer._mm_to_dots(25.4) == 360


class TestLabelPrinterPrint:
    """Test the complete print workflow."""

    def test_print_sends_data(
        self, mock_connection: MockConnection, sample_image_with_content: Image.Image
    ) -> None:
        """Test that print sends data to the connection."""
        printer = PTE550W(mock_connection, use_compression=True)
        label = Label(sample_image_with_content, Tape12mm)
        printer.print(label)
        # Should have sent data
        assert len(mock_connection.data) > 0
        # Should start with invalidate (null bytes)
        assert mock_connection.data[:50] == b"\x00" * 50

    def test_print_with_custom_margin(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test print with custom margin."""
        printer = PTE550W(mock_connection)
        label = Label(sample_image, Tape12mm)
        printer.print(label, margin_mm=5.0)
        assert len(mock_connection.data) > 0

    def test_print_invalid_margin_too_small(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that margin below minimum raises ValueError."""
        printer = PTE550W(mock_connection)
        label = Label(sample_image, Tape12mm)
        with pytest.raises(ValueError, match="Margin must be between"):
            printer.print(label, margin_mm=0.5)

    def test_print_invalid_margin_too_large(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that margin above maximum raises ValueError."""
        printer = PTE550W(mock_connection)
        label = Label(sample_image, Tape12mm)
        with pytest.raises(ValueError, match="Margin must be between"):
            printer.print(label, margin_mm=200.0)

    def test_print_unsupported_tape(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that printing with unsupported tape raises ValueError."""
        printer = PTE550W(mock_connection)
        label = Label(sample_image, Tape36mm)  # E550W doesn't support 36mm
        with pytest.raises(ValueError, match="not supported"):
            printer.print(label)

    def test_print_with_high_resolution(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test printing in high resolution mode."""
        printer = PTE550W(mock_connection)
        label = Label(sample_image, Tape12mm)
        printer.print(label, high_resolution=True)
        assert len(mock_connection.data) > 0

    def test_print_ends_with_print_command(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that print data ends with print command (0x1a) and initialize."""
        printer = PTE550W(mock_connection, use_compression=True)
        label = Label(sample_image, Tape12mm)
        printer.print(label)
        # Should contain print command
        assert b"\x1a" in mock_connection.data


class TestImagePreparation:
    """Test image preparation methods."""

    def test_prepare_image_returns_1bit(self, mock_connection: MockConnection) -> None:
        """Test that _prepare_image returns a 1-bit image."""
        printer = PTE550W(mock_connection)
        img = Image.new("RGB", (100, 50), color=(255, 255, 255))
        tape = Tape12mm()
        config = printer.get_tape_config(tape)
        img_1bit = printer._prepare_image(img, config)
        assert img_1bit.mode == "1"

    def test_prepare_image_matches_print_pins_height(self, mock_connection: MockConnection) -> None:
        """Test that prepared image height matches print_pins."""
        printer = PTE550W(mock_connection)
        img = Image.new("RGB", (100, 50), color=(255, 255, 255))
        tape = Tape12mm()
        config = printer.get_tape_config(tape)
        img_1bit = printer._prepare_image(img, config)
        assert img_1bit.height == config.print_pins

    def test_generate_raster_correct_length(self, mock_connection: MockConnection) -> None:
        """Test that raster data has correct length."""
        printer = PTE550W(mock_connection)
        img = Image.new("RGB", (100, 50), color=(255, 255, 255))
        tape = Tape12mm()
        config = printer.get_tape_config(tape)
        img_1bit = printer._prepare_image(img, config)
        raster = printer._generate_raster(img_1bit, config)
        # Each column should have BYTES_PER_LINE bytes
        expected_length = img_1bit.width * printer.BYTES_PER_LINE
        assert len(raster) == expected_length


class TestLabelPrinterPrintMulti:
    """Test the print_multi workflow for multiple labels."""

    def test_print_multi_sends_data(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that print_multi sends data to the connection."""
        printer = PTE550W(mock_connection, use_compression=True)
        labels = [
            Label(sample_image, Tape12mm),
            Label(sample_image, Tape12mm),
        ]
        printer.print_multi(labels)
        # Should have sent data
        assert len(mock_connection.data) > 0
        # Should start with invalidate (null bytes)
        assert mock_connection.data[:50] == b"\x00" * 50

    def test_print_multi_single_label(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that print_multi with a single label works correctly."""
        printer = PTE550W(mock_connection, use_compression=True)
        labels = [Label(sample_image, Tape12mm)]
        printer.print_multi(labels)
        # Should have sent data
        assert len(mock_connection.data) > 0
        # Single label should end with print command (0x1a)
        assert b"\x1a" in mock_connection.data

    def test_print_multi_empty_list_raises_error(self, mock_connection: MockConnection) -> None:
        """Test that print_multi with empty list raises ValueError."""
        printer = PTE550W(mock_connection)
        with pytest.raises(ValueError, match="(?i)at least one label"):
            printer.print_multi([])

    def test_print_multi_mismatched_tapes_raises_error(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that print_multi with different tape types raises ValueError."""
        printer = PTE550W(mock_connection)
        labels = [
            Label(sample_image, Tape12mm),
            Label(sample_image, Tape6mm),
        ]
        with pytest.raises(ValueError, match="same tape type"):
            printer.print_multi(labels)

    def test_print_multi_contains_form_feed_between_labels(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that multi-label print has form feed (0x0C) between labels."""
        printer = PTE550W(mock_connection, use_compression=True)
        labels = [
            Label(sample_image, Tape12mm),
            Label(sample_image, Tape12mm),
        ]
        printer.print_multi(labels)
        # Form feed (0x0C) should appear between labels (not at end)
        assert b"\x0c" in mock_connection.data

    def test_print_multi_ends_with_print_command(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that multi-label print ends with print command (0x1a)."""
        printer = PTE550W(mock_connection, use_compression=True)
        labels = [
            Label(sample_image, Tape12mm),
            Label(sample_image, Tape12mm),
        ]
        printer.print_multi(labels)
        # Should contain final print command
        assert b"\x1a" in mock_connection.data

    def test_print_multi_unsupported_tape(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test that printing with unsupported tape raises ValueError."""
        printer = PTE550W(mock_connection)
        labels = [
            Label(sample_image, Tape36mm),  # E550W doesn't support 36mm
            Label(sample_image, Tape36mm),
        ]
        with pytest.raises(ValueError, match="not supported"):
            printer.print_multi(labels)

    def test_print_multi_with_custom_margin(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test print_multi with custom margin."""
        printer = PTE550W(mock_connection)
        labels = [
            Label(sample_image, Tape12mm),
            Label(sample_image, Tape12mm),
        ]
        printer.print_multi(labels, margin_mm=5.0)
        assert len(mock_connection.data) > 0

    def test_print_multi_with_high_resolution(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Test print_multi in high resolution mode."""
        printer = PTE550W(mock_connection)
        labels = [
            Label(sample_image, Tape12mm),
            Label(sample_image, Tape12mm),
        ]
        printer.print_multi(labels, high_resolution=True)
        assert len(mock_connection.data) > 0


def _find_advanced_mode_byte(data: bytes) -> int:
    """Return the mode byte from the ESC i K command in a print payload.

    The ESC i K command is ``1B 69 4B <mode>``. Locates the last
    occurrence (per-page sequences may contain more than one) and
    returns the byte that follows.
    """
    marker = b"\x1b\x69\x4b"
    idx = data.rfind(marker)
    assert idx != -1, "ESC i K not found in payload"
    return data[idx + 3]


def _find_mode_settings_byte(data: bytes) -> int:
    """Return the mode byte from the ESC i M command in a print payload."""
    marker = b"\x1b\x69\x4d"
    idx = data.rfind(marker)
    assert idx != -1, "ESC i M not found in payload"
    return data[idx + 3]


class TestLabelPrinterCapabilityFlags:
    """Test the SUPPORTS_*/DEFAULT_* class attributes for mirror/chain/special-tape."""

    def test_default_capability_flags_on_base_class(self) -> None:
        """LabelPrinter base class declares the new features as supported."""
        from ptouch.printer import LabelPrinter

        assert LabelPrinter.SUPPORTS_MIRROR_PRINT is True
        assert LabelPrinter.SUPPORTS_CHAIN_PRINTING is True
        assert LabelPrinter.SUPPORTS_SPECIAL_TAPE is True

    def test_default_values_on_base_class(self) -> None:
        """LabelPrinter base class defaults the new features to off."""
        from ptouch.printer import LabelPrinter

        assert LabelPrinter.DEFAULT_MIRROR_PRINT is False
        assert LabelPrinter.DEFAULT_CHAIN_PRINTING is False
        assert LabelPrinter.DEFAULT_SPECIAL_TAPE is False

    def test_pte550w_inherits_capability_flags(self) -> None:
        """PTE550W inherits the new capability flags from the base."""
        assert PTE550W.SUPPORTS_MIRROR_PRINT is True
        assert PTE550W.SUPPORTS_CHAIN_PRINTING is True
        assert PTE550W.SUPPORTS_SPECIAL_TAPE is True

    def test_ptp750w_inherits_capability_flags(self) -> None:
        """PTP750W inherits the new capability flags from the base."""
        assert PTP750W.SUPPORTS_MIRROR_PRINT is True
        assert PTP750W.SUPPORTS_CHAIN_PRINTING is True
        assert PTP750W.SUPPORTS_SPECIAL_TAPE is True


class TestCmdAdvancedModeSpecialTape:
    """Test ESC i K bit 4 (special-tape no-cut) handling."""

    @pytest.fixture
    def printer(self, mock_connection: MockConnection) -> PTE550W:
        """Provide a PTE550W instance."""
        return PTE550W(mock_connection)

    def test_special_tape_off_by_default(self, printer: PTE550W) -> None:
        """Bit 4 is clear when special_tape is not passed."""
        cmd = printer._cmd_advanced_mode_settings()
        assert cmd[3] & (1 << 4) == 0

    def test_special_tape_on_sets_bit_4(self, printer: PTE550W) -> None:
        """Bit 4 is set when special_tape=True."""
        cmd = printer._cmd_advanced_mode_settings(special_tape=True)
        assert cmd[:3] == b"\x1b\x69\x4b"
        assert cmd[3] & (1 << 4) != 0

    def test_special_tape_with_half_cut_and_chain(self, printer: PTE550W) -> None:
        """Bits combine without interfering with each other."""
        cmd = printer._cmd_advanced_mode_settings(
            half_cut=True,
            chain_printing=True,
            high_resolution=True,
            special_tape=True,
        )
        # bit 2 = half cut
        assert cmd[3] & (1 << 2) != 0
        # bit 3 = NO chain printing; chain_printing=True clears it
        assert cmd[3] & (1 << 3) == 0
        # bit 4 = special tape
        assert cmd[3] & (1 << 4) != 0
        # bit 6 = high resolution
        assert cmd[3] & (1 << 6) != 0


class TestCmdModeSettingsMirror:
    """Test ESC i M bit 7 (mirror printing) handling."""

    @pytest.fixture
    def printer(self, mock_connection: MockConnection) -> PTE550W:
        """Provide a PTE550W instance."""
        return PTE550W(mock_connection)

    def test_mirror_off_by_default(self, printer: PTE550W) -> None:
        """Bit 7 is clear when mirror_print is not passed."""
        cmd = printer._cmd_mode_settings(auto_cut=True)
        assert cmd[3] & (1 << 7) == 0

    def test_mirror_on_sets_bit_7(self, printer: PTE550W) -> None:
        """Bit 7 is set when mirror_print=True."""
        cmd = printer._cmd_mode_settings(auto_cut=True, mirror_print=True)
        assert cmd[:3] == b"\x1b\x69\x4d"
        assert cmd[3] & (1 << 7) != 0


class TestPrintNewKwargs:
    """Test that print() honors mirror/chain/special_tape kwargs end-to-end."""

    def test_print_with_mirror_sets_bit_7_in_mode(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print(mirror=True) results in ESC i M bit 7 set in the sent data."""
        printer = PTE550W(mock_connection)
        printer.print(Label(sample_image, Tape12mm), mirror=True)
        mode_byte = _find_mode_settings_byte(mock_connection.data)
        assert mode_byte & (1 << 7) != 0

    def test_print_without_mirror_clears_bit_7(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print() with no mirror kwarg leaves ESC i M bit 7 clear."""
        printer = PTE550W(mock_connection)
        printer.print(Label(sample_image, Tape12mm))
        mode_byte = _find_mode_settings_byte(mock_connection.data)
        assert mode_byte & (1 << 7) == 0

    def test_print_with_chain_clears_no_chain_bit(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print(chain=True) clears ESC i K bit 3 (the no-chain bit is INVERTED)."""
        printer = PTE550W(mock_connection)
        printer.print(Label(sample_image, Tape12mm), chain=True)
        mode_byte = _find_advanced_mode_byte(mock_connection.data)
        # bit 3 is "NO chain printing"; chain=True means it should be 0
        assert mode_byte & (1 << 3) == 0

    def test_print_without_chain_sets_no_chain_bit(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print() with no chain kwarg sets ESC i K bit 3 (feed+cut after page)."""
        printer = PTE550W(mock_connection)
        printer.print(Label(sample_image, Tape12mm))
        mode_byte = _find_advanced_mode_byte(mock_connection.data)
        assert mode_byte & (1 << 3) != 0

    def test_print_with_special_tape_sets_bit_4(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print(special_tape=True) sets ESC i K bit 4."""
        printer = PTE550W(mock_connection)
        printer.print(Label(sample_image, Tape12mm), special_tape=True)
        mode_byte = _find_advanced_mode_byte(mock_connection.data)
        assert mode_byte & (1 << 4) != 0

    def test_print_without_special_tape_clears_bit_4(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print() with no special_tape kwarg leaves ESC i K bit 4 clear."""
        printer = PTE550W(mock_connection)
        printer.print(Label(sample_image, Tape12mm))
        mode_byte = _find_advanced_mode_byte(mock_connection.data)
        assert mode_byte & (1 << 4) == 0


class TestPrintDefaultsHonoredFromClass:
    """Test that DEFAULT_* class attrs flow through when kwargs are omitted."""

    def test_subclass_default_mirror_print_true(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """A subclass with DEFAULT_MIRROR_PRINT=True mirrors by default."""

        class MirroredP750W(PTP750W):
            DEFAULT_MIRROR_PRINT: bool = True

        printer = MirroredP750W(mock_connection)
        printer.print(Label(sample_image, Tape12mm))
        mode_byte = _find_mode_settings_byte(mock_connection.data)
        assert mode_byte & (1 << 7) != 0

    def test_runtime_kwarg_overrides_subclass_default(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Explicit mirror=False overrides a subclass DEFAULT_MIRROR_PRINT=True."""

        class MirroredP750W(PTP750W):
            DEFAULT_MIRROR_PRINT: bool = True

        printer = MirroredP750W(mock_connection)
        printer.print(Label(sample_image, Tape12mm), mirror=False)
        mode_byte = _find_mode_settings_byte(mock_connection.data)
        assert mode_byte & (1 << 7) == 0


class TestPrintMultiForwardsNewKwargs:
    """Test that print_multi() forwards mirror/chain/special_tape to print()."""

    def test_print_multi_with_mirror(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print_multi(mirror=True) sets ESC i M bit 7 on every page."""
        printer = PTE550W(mock_connection)
        labels = [Label(sample_image, Tape12mm), Label(sample_image, Tape12mm)]
        printer.print_multi(labels, mirror=True)
        # Every ESC i M occurrence should have bit 7 set
        data = mock_connection.data
        idx = 0
        marker = b"\x1b\x69\x4d"
        found = 0
        while True:
            idx = data.find(marker, idx)
            if idx == -1:
                break
            assert data[idx + 3] & (1 << 7) != 0
            found += 1
            idx += len(marker)
        assert found >= 2  # one per page

    def test_print_multi_with_chain(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print_multi(chain=True) clears ESC i K bit 3 on every page."""
        printer = PTE550W(mock_connection)
        labels = [Label(sample_image, Tape12mm), Label(sample_image, Tape12mm)]
        printer.print_multi(labels, chain=True)
        data = mock_connection.data
        idx = 0
        marker = b"\x1b\x69\x4b"
        found = 0
        while True:
            idx = data.find(marker, idx)
            if idx == -1:
                break
            assert data[idx + 3] & (1 << 3) == 0
            found += 1
            idx += len(marker)
        assert found >= 2

    def test_print_multi_with_special_tape(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print_multi(special_tape=True) sets ESC i K bit 4 on every page."""
        printer = PTE550W(mock_connection)
        labels = [Label(sample_image, Tape12mm), Label(sample_image, Tape12mm)]
        printer.print_multi(labels, special_tape=True)
        data = mock_connection.data
        idx = 0
        marker = b"\x1b\x69\x4b"
        found = 0
        while True:
            idx = data.find(marker, idx)
            if idx == -1:
                break
            assert data[idx + 3] & (1 << 4) != 0
            found += 1
            idx += len(marker)
        assert found >= 2


class TestCapabilityEnforcement:
    """Test that SUPPORTS_* flags are enforced in print()/print_multi()."""

    def test_explicit_unsupported_feature_raises(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Explicitly requesting a feature the model lacks raises ValueError."""

        class NoMirrorP750W(PTP750W):
            SUPPORTS_MIRROR_PRINT = False

        printer = NoMirrorP750W(mock_connection)
        with pytest.raises(ValueError, match="does not support mirror printing"):
            printer.print(Label(sample_image, Tape12mm), mirror=True)
        # No print payload (raster transfer / print command) should be emitted.
        assert b"\x47" not in mock_connection.data  # raster graphics transfer
        assert b"\x1a" not in mock_connection.data and b"\x0c" not in mock_connection.data

    def test_unsupported_default_is_clamped_not_raised(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """A True DEFAULT_* on an unsupported feature is forced off, not raised."""

        class NoMirrorDefaultOnP750W(PTP750W):
            SUPPORTS_MIRROR_PRINT = False
            DEFAULT_MIRROR_PRINT = True

        printer = NoMirrorDefaultOnP750W(mock_connection)
        # No kwarg → default path → must not raise, and bit 7 stays clear.
        printer.print(Label(sample_image, Tape12mm))
        mode_byte = _find_mode_settings_byte(mock_connection.data)
        assert mode_byte & (1 << 7) == 0

    def test_explicit_false_on_unsupported_is_allowed(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Explicitly disabling an unsupported feature is fine (no raise)."""

        class NoMirrorP750W(PTP750W):
            SUPPORTS_MIRROR_PRINT = False

        printer = NoMirrorP750W(mock_connection)
        printer.print(Label(sample_image, Tape12mm), mirror=False)  # must not raise
        mode_byte = _find_mode_settings_byte(mock_connection.data)
        assert mode_byte & (1 << 7) == 0

    def test_print_multi_half_cut_clamped_for_unsupported(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """print_multi() default half_cut clamps to full-cut (no raise) when unsupported."""
        from ptouch.printers import PTP710BT

        printer = PTP710BT(mock_connection)
        labels = [Label(sample_image, Tape12mm), Label(sample_image, Tape12mm)]
        # PTP710BT.SUPPORTS_HALF_CUT is False; the default half_cut=True must
        # clamp rather than raise, and every page's half-cut bit (2) stays clear.
        printer.print_multi(labels)
        data = mock_connection.data
        marker = b"\x1b\x69\x4b"
        idx = 0
        found = 0
        while True:
            idx = data.find(marker, idx)
            if idx == -1:
                break
            assert data[idx + 3] & (1 << 2) == 0
            found += 1
            idx += len(marker)
        assert found >= 2


class TestHighResolutionCapability:
    """Test that the high-resolution capability is enforced like the SUPPORTS_* flags."""

    def test_p910bt_has_no_high_resolution_mode(self) -> None:
        """PT-P910BT declares no high-resolution mode, unlike the rest of the series."""
        assert PTP910BT.RESOLUTION_DPI_HIGH == 0
        assert PTP900.RESOLUTION_DPI_HIGH == 720

    def test_supports_high_resolution_reflects_the_model(
        self, mock_connection: MockConnection
    ) -> None:
        """supports_high_resolution follows RESOLUTION_DPI_HIGH per model."""
        assert PTP900(mock_connection).supports_high_resolution is True
        assert PTP910BT(mock_connection).supports_high_resolution is False

    def test_explicit_request_on_unsupported_model_raises(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Asking for high resolution on a model without it raises before any output."""
        printer = PTP910BT(mock_connection)
        with pytest.raises(ValueError, match="does not support high-resolution printing"):
            printer.print(Label(sample_image, Tape12mm), high_resolution=True)
        # No print payload may be emitted: doubling the raster lines without a
        # matching feed resolution would print the label at twice the length.
        # (The invalidate/initialize sequence is already sent by __init__.)
        assert b"\x47" not in mock_connection.data  # raster graphics transfer
        assert b"\x1a" not in mock_connection.data and b"\x0c" not in mock_connection.data

    def test_constructor_request_on_unsupported_model_raises(
        self, mock_connection: MockConnection
    ) -> None:
        """An explicit constructor request raises too, not just the print() kwarg."""
        with pytest.raises(ValueError, match="does not support high-resolution printing"):
            PTP910BT(mock_connection, high_resolution=True)
        # The failure happens before the connection is opened, so nothing is sent.
        assert mock_connection.data == b""

    def test_unsupported_class_default_is_clamped(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """A True DEFAULT_HIGH_RESOLUTION on an unsupported model is forced off."""

        class HighResDefaultOnP910BT(PTP910BT):
            DEFAULT_HIGH_RESOLUTION = True

        printer = HighResDefaultOnP910BT(mock_connection)
        assert printer.high_resolution is False  # resolved once, honestly
        printer.print(Label(sample_image, Tape12mm))
        assert _find_advanced_mode_byte(mock_connection.data) & (1 << 6) == 0

    def test_supported_model_keeps_constructor_request(
        self, mock_connection: MockConnection
    ) -> None:
        """A constructor request on a model that supports it is preserved."""
        assert PTP900(mock_connection, high_resolution=True).high_resolution is True

    def test_explicit_false_on_unsupported_model_is_allowed(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """Explicitly disabling high resolution on a model without it is fine."""
        printer = PTP910BT(mock_connection)
        printer.print(Label(sample_image, Tape12mm), high_resolution=False)
        assert _find_advanced_mode_byte(mock_connection.data) & (1 << 6) == 0

    def test_supported_model_still_sets_the_bit(
        self, mock_connection: MockConnection, sample_image: Image.Image
    ) -> None:
        """A model that does support high resolution still emits ESC i K bit 6."""
        printer = PTP900(mock_connection)
        printer.print(Label(sample_image, Tape12mm), high_resolution=True)
        assert _find_advanced_mode_byte(mock_connection.data) & (1 << 6) != 0
