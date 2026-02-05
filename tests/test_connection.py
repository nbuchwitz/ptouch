# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Tests for the ptouch.connection module."""

import socket
from unittest.mock import MagicMock, patch

import pytest

from ptouch.connection import (
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


class MockPrinter:
    """Mock printer for testing USB connections."""

    USB_PRODUCT_ID = 0x1234


class MockPrinterNoUSB:
    """Mock printer without USB_PRODUCT_ID for testing error case."""

    pass


class TestPrinterConnectionError:
    """Test PrinterConnectionError exception."""

    def test_exception_message(self) -> None:
        """Test that exception stores message correctly."""
        error = PrinterConnectionError("Test error message")
        assert str(error) == "Test error message"
        assert error.original_error is None

    def test_exception_with_original_error(self) -> None:
        """Test that exception stores original error."""
        original = ValueError("Original error")
        error = PrinterConnectionError("Wrapped error", original_error=original)
        assert str(error) == "Wrapped error"
        assert error.original_error is original

    def test_exception_is_importable_from_package(self) -> None:
        """Test that PrinterConnectionError can be imported from ptouch."""
        from ptouch import PrinterConnectionError as ImportedError

        assert ImportedError is PrinterConnectionError


class TestPrinterExceptionHierarchy:
    """Test exception hierarchy and inheritance."""

    def test_all_exceptions_inherit_from_base(self) -> None:
        """Test that all specific exceptions inherit from PrinterConnectionError."""
        assert issubclass(PrinterNotFoundError, PrinterConnectionError)
        assert issubclass(PrinterPermissionError, PrinterConnectionError)
        assert issubclass(PrinterNetworkError, PrinterConnectionError)
        assert issubclass(PrinterTimeoutError, PrinterConnectionError)
        assert issubclass(PrinterWriteError, PrinterConnectionError)

    def test_exceptions_are_importable_from_package(self) -> None:
        """Test that all exceptions can be imported from ptouch package."""
        from ptouch import (
            PrinterConnectionError as Base,
            PrinterNetworkError as Network,
            PrinterNotFoundError as NotFound,
            PrinterPermissionError as Permission,
            PrinterTimeoutError as Timeout,
            PrinterWriteError as Write,
        )

        assert Base is PrinterConnectionError
        assert Network is PrinterNetworkError
        assert NotFound is PrinterNotFoundError
        assert Permission is PrinterPermissionError
        assert Timeout is PrinterTimeoutError
        assert Write is PrinterWriteError

    def test_specific_exception_can_be_caught_specifically(self) -> None:
        """Test that specific exceptions can be caught without catching all."""
        with pytest.raises(PrinterNotFoundError):
            raise PrinterNotFoundError("Device not found")

        with pytest.raises(PrinterConnectionError):
            raise PrinterNotFoundError("Device not found")

    def test_exception_with_original_error(self) -> None:
        """Test that all exceptions support original_error parameter."""
        original = ValueError("Original")
        errors = [
            PrinterNotFoundError("Not found", original_error=original),
            PrinterPermissionError("Permission denied", original_error=original),
            PrinterNetworkError("Network error", original_error=original),
            PrinterTimeoutError("Timeout", original_error=original),
            PrinterWriteError("Write failed", original_error=original),
        ]
        for error in errors:
            assert error.original_error is original


class TestConnectionUSBInit:
    """Test ConnectionUSB initialization."""

    def test_usb_connection_init_no_args(self) -> None:
        """Test that ConnectionUSB can be created without arguments."""
        conn = ConnectionUSB()
        assert conn._device is None
        assert conn._ep_in is None
        assert conn._ep_out is None

    def test_usb_connect_requires_product_id(self) -> None:
        """Test that connect() raises error if printer has no USB_PRODUCT_ID."""
        conn = ConnectionUSB()
        with pytest.raises(PrinterConnectionError) as exc_info:
            conn.connect(MockPrinterNoUSB())  # type: ignore[arg-type]

        assert "USB_PRODUCT_ID" in str(exc_info.value)

    def test_usb_connect_with_mock_printer(self) -> None:
        """Test that connect() uses printer's USB_PRODUCT_ID."""
        with patch("usb.core.find") as mock_find:
            mock_device = MagicMock()
            mock_find.return_value = mock_device
            mock_device.is_kernel_driver_active.return_value = False

            mock_intf = MagicMock()
            mock_intf.bInterfaceClass = 7

            mock_cfg = MagicMock()
            mock_device.get_active_configuration.return_value = mock_cfg

            with patch("usb.util.find_descriptor") as mock_find_desc:
                mock_ep = MagicMock()
                mock_find_desc.return_value = mock_ep

                conn = ConnectionUSB()
                conn.connect(MockPrinter())  # type: ignore[arg-type]

                # Should have called usb.core.find with the product ID from MockPrinter
                mock_find.assert_called_once()
                call_kwargs = mock_find.call_args[1]
                assert call_kwargs["idProduct"] == 0x1234


class TestConnectionNetworkInit:
    """Test ConnectionNetwork initialization and connect()."""

    def test_network_init_stores_params(self) -> None:
        """Test that __init__ stores parameters without connecting."""
        conn = ConnectionNetwork("192.168.1.100", timeout=10.0)
        assert conn.host == "192.168.1.100"
        assert conn.port == 9100
        assert conn.timeout == 10.0
        assert conn._socket is None  # Not connected yet

    def test_default_timeout(self) -> None:
        """Test that default timeout is 5.0 seconds."""
        conn = ConnectionNetwork("192.168.1.100")
        assert conn.timeout == 5.0

    def test_connect_establishes_socket(self) -> None:
        """Test that connect() creates and configures socket."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_socket.return_value = mock_sock

            conn = ConnectionNetwork("192.168.1.100", timeout=10.0)
            conn.connect(MockPrinter())  # type: ignore[arg-type]

            mock_sock.settimeout.assert_called_with(10.0)
            mock_sock.connect.assert_called_once_with(("192.168.1.100", 9100))

    def test_connection_timeout_raises_printer_error(self) -> None:
        """Test that connection timeout raises PrinterConnectionError."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_socket.return_value = mock_sock
            mock_sock.connect.side_effect = socket.timeout("timed out")

            conn = ConnectionNetwork("192.168.1.100", timeout=5.0)
            with pytest.raises(PrinterConnectionError) as exc_info:
                conn.connect(MockPrinter())  # type: ignore[arg-type]

            assert "timed out" in str(exc_info.value)
            assert "192.168.1.100:9100" in str(exc_info.value)
            assert isinstance(exc_info.value.original_error, socket.timeout)
            mock_sock.close.assert_called_once()

    def test_connection_refused_raises_printer_error(self) -> None:
        """Test that connection refused raises PrinterConnectionError."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_socket.return_value = mock_sock
            mock_sock.connect.side_effect = ConnectionRefusedError("Connection refused")

            conn = ConnectionNetwork("192.168.1.100")
            with pytest.raises(PrinterConnectionError) as exc_info:
                conn.connect(MockPrinter())  # type: ignore[arg-type]

            assert "refused" in str(exc_info.value).lower()
            assert "192.168.1.100:9100" in str(exc_info.value)
            assert isinstance(exc_info.value.original_error, ConnectionRefusedError)
            mock_sock.close.assert_called_once()

    def test_hostname_resolution_error_raises_printer_error(self) -> None:
        """Test that hostname resolution failure raises PrinterConnectionError."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_socket.return_value = mock_sock
            mock_sock.connect.side_effect = socket.gaierror(8, "Name not resolved")

            conn = ConnectionNetwork("invalid.hostname.local")
            with pytest.raises(PrinterConnectionError) as exc_info:
                conn.connect(MockPrinter())  # type: ignore[arg-type]

            assert "invalid.hostname.local" in str(exc_info.value)
            assert "resolve" in str(exc_info.value).lower()
            assert isinstance(exc_info.value.original_error, socket.gaierror)
            mock_sock.close.assert_called_once()

    def test_generic_os_error_raises_printer_error(self) -> None:
        """Test that generic OSError raises PrinterConnectionError."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_socket.return_value = mock_sock
            mock_sock.connect.side_effect = OSError("Network unreachable")

            conn = ConnectionNetwork("192.168.1.100")
            with pytest.raises(PrinterConnectionError) as exc_info:
                conn.connect(MockPrinter())  # type: ignore[arg-type]

            assert "192.168.1.100:9100" in str(exc_info.value)
            assert isinstance(exc_info.value.original_error, OSError)
            mock_sock.close.assert_called_once()


class TestConnectionNetworkWrite:
    """Test ConnectionNetwork write method error handling."""

    @pytest.fixture
    def connected_network(self) -> ConnectionNetwork:
        """Create a ConnectionNetwork with mocked socket."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_socket.return_value = mock_sock
            conn = ConnectionNetwork("192.168.1.100")
            conn.connect(MockPrinter())  # type: ignore[arg-type]
            return conn

    def test_write_timeout_raises_printer_error(self, connected_network: ConnectionNetwork) -> None:
        """Test that write timeout raises PrinterConnectionError."""
        assert connected_network._socket is not None
        connected_network._socket.sendall.side_effect = socket.timeout("timed out")

        with pytest.raises(PrinterConnectionError) as exc_info:
            connected_network.write(b"test data")

        assert "timed out" in str(exc_info.value).lower()
        assert isinstance(exc_info.value.original_error, socket.timeout)

    def test_write_broken_pipe_raises_printer_error(
        self, connected_network: ConnectionNetwork
    ) -> None:
        """Test that broken pipe raises PrinterConnectionError."""
        assert connected_network._socket is not None
        connected_network._socket.sendall.side_effect = BrokenPipeError("Broken pipe")

        with pytest.raises(PrinterConnectionError) as exc_info:
            connected_network.write(b"test data")

        assert "lost" in str(exc_info.value).lower()
        assert isinstance(exc_info.value.original_error, BrokenPipeError)

    def test_write_connection_reset_raises_printer_error(
        self, connected_network: ConnectionNetwork
    ) -> None:
        """Test that connection reset raises PrinterConnectionError."""
        assert connected_network._socket is not None
        connected_network._socket.sendall.side_effect = ConnectionResetError("Connection reset")

        with pytest.raises(PrinterConnectionError) as exc_info:
            connected_network.write(b"test data")

        assert "lost" in str(exc_info.value).lower()
        assert isinstance(exc_info.value.original_error, ConnectionResetError)

    def test_write_not_connected_raises_printer_error(self) -> None:
        """Test that write before connect raises PrinterConnectionError."""
        conn = ConnectionNetwork("192.168.1.100")
        with pytest.raises(PrinterConnectionError) as exc_info:
            conn.write(b"test data")

        assert "Not connected" in str(exc_info.value)


class TestConnectionNetworkRead:
    """Test ConnectionNetwork read method error handling."""

    @pytest.fixture
    def connected_network(self) -> ConnectionNetwork:
        """Create a ConnectionNetwork with mocked socket."""
        with patch("socket.socket") as mock_socket:
            mock_sock = MagicMock()
            mock_socket.return_value = mock_sock
            conn = ConnectionNetwork("192.168.1.100")
            conn.connect(MockPrinter())  # type: ignore[arg-type]
            return conn

    def test_read_timeout_raises_printer_error(self, connected_network: ConnectionNetwork) -> None:
        """Test that read timeout raises PrinterConnectionError."""
        assert connected_network._socket is not None
        connected_network._socket.recv.side_effect = socket.timeout("timed out")

        with pytest.raises(PrinterConnectionError) as exc_info:
            connected_network.read()

        assert "timed out" in str(exc_info.value).lower()
        assert isinstance(exc_info.value.original_error, socket.timeout)

    def test_read_broken_pipe_raises_printer_error(
        self, connected_network: ConnectionNetwork
    ) -> None:
        """Test that broken pipe raises PrinterConnectionError."""
        assert connected_network._socket is not None
        connected_network._socket.recv.side_effect = BrokenPipeError("Broken pipe")

        with pytest.raises(PrinterConnectionError) as exc_info:
            connected_network.read()

        assert "lost" in str(exc_info.value).lower()
        assert isinstance(exc_info.value.original_error, BrokenPipeError)

    def test_read_not_connected_raises_printer_error(self) -> None:
        """Test that read before connect raises PrinterConnectionError."""
        conn = ConnectionNetwork("192.168.1.100")
        with pytest.raises(PrinterConnectionError) as exc_info:
            conn.read()

        assert "Not connected" in str(exc_info.value)


class TestParseUsbUri:
    """Test parse_usb_uri function."""

    def test_parse_vendor_product(self) -> None:
        """Test parsing URI with vendor and product."""
        vendor, product, serial = parse_usb_uri("usb://0x04f9:0x2086")
        assert vendor == 0x04F9
        assert product == 0x2086
        assert serial is None

    def test_parse_vendor_product_serial(self) -> None:
        """Test parsing URI with vendor, product and serial."""
        vendor, product, serial = parse_usb_uri("usb://0x04f9:0x2086/A1B2C3D4E5")
        assert vendor == 0x04F9
        assert product == 0x2086
        assert serial == "A1B2C3D4E5"

    def test_parse_product_only(self) -> None:
        """Test parsing URI with product only (no vendor)."""
        vendor, product, serial = parse_usb_uri("usb://:0x2086")
        assert vendor is None
        assert product == 0x2086
        assert serial is None

    def test_parse_product_serial_no_vendor(self) -> None:
        """Test parsing URI with product and serial but no vendor."""
        vendor, product, serial = parse_usb_uri("usb://:0x2086/ABC123")
        assert vendor is None
        assert product == 0x2086
        assert serial == "ABC123"

    def test_parse_uppercase_hex(self) -> None:
        """Test parsing URI with uppercase hex values."""
        vendor, product, serial = parse_usb_uri("usb://0x04F9:0x2086")
        assert vendor == 0x04F9
        assert product == 0x2086

    def test_parse_serial_hex(self) -> None:
        """Test parsing URI with hex serial number."""
        vendor, product, serial = parse_usb_uri("usb://:0x2086/00FF1A2B3C")
        assert serial == "00FF1A2B3C"

    def test_invalid_uri_no_scheme(self) -> None:
        """Test that URI without usb:// raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            parse_usb_uri("0x04f9:0x2086")
        assert "Invalid USB URI format" in str(exc_info.value)

    def test_invalid_uri_wrong_scheme(self) -> None:
        """Test that URI with wrong scheme raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            parse_usb_uri("http://0x04f9:0x2086")
        assert "Invalid USB URI format" in str(exc_info.value)

    def test_invalid_uri_no_product(self) -> None:
        """Test that URI without product raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            parse_usb_uri("usb://0x04f9:")
        assert "Invalid USB URI format" in str(exc_info.value)

    def test_invalid_uri_empty(self) -> None:
        """Test that empty URI raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            parse_usb_uri("")
        assert "Invalid USB URI format" in str(exc_info.value)

    def test_invalid_uri_non_hex_serial(self) -> None:
        """Test that URI with non-hex serial raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            parse_usb_uri("usb://:0x2086/SN-123")
        assert "Invalid USB URI format" in str(exc_info.value)

    def test_parse_usb_uri_importable_from_package(self) -> None:
        """Test that parse_usb_uri can be imported from ptouch."""
        from ptouch import parse_usb_uri as imported_func

        assert imported_func is parse_usb_uri


class TestConnectionUSBParams:
    """Test ConnectionUSB with explicit vendor/product/serial parameters."""

    def test_init_with_no_params(self) -> None:
        """Test default initialization stores None values."""
        conn = ConnectionUSB()
        assert conn._vendor_id is None
        assert conn._product_id is None
        assert conn._serial is None

    def test_init_with_product_id(self) -> None:
        """Test initialization with product_id only."""
        conn = ConnectionUSB(product_id=0x2086)
        assert conn._vendor_id is None
        assert conn._product_id == 0x2086
        assert conn._serial is None

    def test_init_with_all_params(self) -> None:
        """Test initialization with all parameters."""
        conn = ConnectionUSB(vendor_id=0x04F9, product_id=0x2086, serial="ABC123")
        assert conn._vendor_id == 0x04F9
        assert conn._product_id == 0x2086
        assert conn._serial == "ABC123"

    def test_connect_uses_explicit_product_id(self) -> None:
        """Test that connect() uses explicit product_id over printer's USB_PRODUCT_ID."""
        with patch("usb.core.find") as mock_find:
            mock_device = MagicMock()
            mock_find.return_value = mock_device
            mock_device.is_kernel_driver_active.return_value = False

            mock_cfg = MagicMock()
            mock_device.get_active_configuration.return_value = mock_cfg

            with patch("usb.util.find_descriptor") as mock_find_desc:
                mock_ep = MagicMock()
                mock_find_desc.return_value = mock_ep

                conn = ConnectionUSB(product_id=0x9999)
                conn.connect(MockPrinter())  # type: ignore[arg-type]

                call_kwargs = mock_find.call_args[1]
                # Should use explicit product_id, not MockPrinter's 0x1234
                assert call_kwargs["idProduct"] == 0x9999

    def test_connect_uses_explicit_vendor_id(self) -> None:
        """Test that connect() uses explicit vendor_id."""
        with patch("usb.core.find") as mock_find:
            mock_device = MagicMock()
            mock_find.return_value = mock_device
            mock_device.is_kernel_driver_active.return_value = False

            mock_cfg = MagicMock()
            mock_device.get_active_configuration.return_value = mock_cfg

            with patch("usb.util.find_descriptor") as mock_find_desc:
                mock_ep = MagicMock()
                mock_find_desc.return_value = mock_ep

                conn = ConnectionUSB(vendor_id=0x1234, product_id=0x5678)
                conn.connect(MockPrinter())  # type: ignore[arg-type]

                call_kwargs = mock_find.call_args[1]
                assert call_kwargs["idVendor"] == 0x1234
                assert call_kwargs["idProduct"] == 0x5678

    def test_connect_uses_serial_number(self) -> None:
        """Test that connect() passes serial_number to usb.core.find."""
        with patch("usb.core.find") as mock_find:
            mock_device = MagicMock()
            mock_find.return_value = mock_device
            mock_device.is_kernel_driver_active.return_value = False

            mock_cfg = MagicMock()
            mock_device.get_active_configuration.return_value = mock_cfg

            with patch("usb.util.find_descriptor") as mock_find_desc:
                mock_ep = MagicMock()
                mock_find_desc.return_value = mock_ep

                conn = ConnectionUSB(product_id=0x2086, serial="ABC123")
                conn.connect(MockPrinter())  # type: ignore[arg-type]

                call_kwargs = mock_find.call_args[1]
                assert call_kwargs["serial_number"] == "ABC123"

    def test_not_found_error_includes_serial(self) -> None:
        """Test that PrinterNotFoundError includes serial when device not found."""
        with patch("usb.core.find") as mock_find:
            mock_find.return_value = None

            conn = ConnectionUSB(product_id=0x2086, serial="ABC123")
            with pytest.raises(PrinterNotFoundError) as exc_info:
                conn.connect(MockPrinter())  # type: ignore[arg-type]

            assert "ABC123" in str(exc_info.value)
            assert "0x2086" in str(exc_info.value).lower()

    def test_connect_without_product_id_uses_printer_class(self) -> None:
        """Test that connect() falls back to printer's USB_PRODUCT_ID."""
        with patch("usb.core.find") as mock_find:
            mock_device = MagicMock()
            mock_find.return_value = mock_device
            mock_device.is_kernel_driver_active.return_value = False

            mock_cfg = MagicMock()
            mock_device.get_active_configuration.return_value = mock_cfg

            with patch("usb.util.find_descriptor") as mock_find_desc:
                mock_ep = MagicMock()
                mock_find_desc.return_value = mock_ep

                conn = ConnectionUSB()  # No explicit product_id
                conn.connect(MockPrinter())  # type: ignore[arg-type]

                call_kwargs = mock_find.call_args[1]
                # Should use MockPrinter's USB_PRODUCT_ID
                assert call_kwargs["idProduct"] == 0x1234
