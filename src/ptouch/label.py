# SPDX-FileCopyrightText: 2024-2026 Nicolai Buchwitz <nb@tipi-net.de>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Label classes for Brother P-touch label printers."""

from enum import Flag, auto

from PIL import Image, ImageDraw, ImageFont

from .tape import Tape


class Label:
    """A label to be printed on a specific tape.

    Attributes
    ----------
    image : PIL.Image.Image
        The image to print.
    tape : Tape
        The tape this label is designed for.
    """

    def __init__(self, image: Image.Image, tape: type[Tape] | Tape) -> None:
        """Initialize a label.

        Parameters
        ----------
        image : PIL.Image.Image
            The image to print.
        tape : type[Tape] | Tape
            The tape class (e.g., Tape36mm) or instance.
        """
        self.image = image
        self.tape = tape() if isinstance(tape, type) else tape

    def prepare(self, height: int, resolution_dpi: int = 180) -> None:
        """Prepare the label for printing.

        Called by the printer before printing. Override in subclasses
        that need deferred rendering (e.g., TextLabel).

        Parameters
        ----------
        height : int
            Print height in pixels (tape_config.print_pins).
        resolution_dpi : int, default 180
            Printer resolution in DPI for mm to pixel conversion.
        """
        pass


class TextLabel(Label):
    """A label containing rendered text.

    The image is rendered automatically when printed, using the correct
    height for the printer/tape combination.
    """

    class Align(Flag):
        """Text alignment options. Combine with | operator, e.g. Align.LEFT | Align.TOP."""

        LEFT = auto()
        HCENTER = auto()
        RIGHT = auto()
        TOP = auto()
        VCENTER = auto()
        BOTTOM = auto()
        # Convenience alias for both centered
        CENTER = HCENTER | VCENTER

    def __init__(
        self,
        text: str,
        tape: type[Tape] | Tape,
        font: str | ImageFont.FreeTypeFont,
        font_size: int | None = None,
        align: "TextLabel.Align | None" = None,
        min_width_mm: float | None = None,
        fixed_width_mm: float | None = None,
        auto_size: bool = True,
    ) -> None:
        """Initialize a text label.

        Parameters
        ----------
        text : str
            Text to render.
        tape : type[Tape] | Tape
            The tape class (e.g., Tape36mm) or instance.
        font : str or ImageFont.FreeTypeFont
            Path to TrueType font file, or a pre-loaded ImageFont object.
        font_size : int or None, optional
            Font size in pixels. Only used when auto_size=False.
        align : TextLabel.Align, default TextLabel.Align.CENTER
            Text alignment. Combine horizontal (LEFT, HCENTER, RIGHT) and
            vertical (TOP, VCENTER, BOTTOM) with |, e.g. Align.LEFT | Align.TOP.
            Use Align.CENTER for both horizontally and vertically centered.
        min_width_mm : float or None, optional
            Minimum label width in millimeters. If specified, the label will
            be padded to at least this width. Ignored when fixed_width_mm is set.
        fixed_width_mm : float or None, optional
            Fixed label width in millimeters. If specified, the label is locked
            to exactly this width and the font is scaled down so the text fits
            within it (it does not expand the label to the text size).
        auto_size : bool, default True
            If True, automatically size the font to 80% of the print height.
            If False, use font_size (for path strings) or the ImageFont's
            built-in size.
        """
        self.text = text
        self.tape = tape() if isinstance(tape, type) else tape
        if not isinstance(font, (str, ImageFont.FreeTypeFont)):
            raise ValueError(
                f"font must be a path string or ImageFont.FreeTypeFont, got {type(font).__name__}"
            )
        self.font = font
        self.font_size = font_size
        self.align = align if align is not None else TextLabel.Align.CENTER
        self.min_width_mm = min_width_mm
        self.fixed_width_mm = fixed_width_mm
        self.auto_size = auto_size
        self._image: Image.Image | None = None

    @property
    def image(self) -> Image.Image:
        """Get the rendered image."""
        if self._image is None:
            raise RuntimeError(
                "TextLabel has not been rendered yet. "
                "Call prepare(height) or let the printer handle it."
            )
        return self._image

    def prepare(self, height: int, resolution_dpi: int = 180) -> None:
        """Render the text to an image.

        Parameters
        ----------
        height : int
            Image height in pixels (tape_config.print_pins).
        resolution_dpi : int, default 180
            Printer resolution in DPI for mm to pixel conversion.
        """
        if self._image is not None:
            return  # Already rendered

        # Build a loader that can re-create the font at an arbitrary size, so we
        # can shrink it to fit a fixed width. can_resize is False for bitmap
        # fonts that cannot be scaled.
        if isinstance(self.font, str):
            if self.auto_size:
                font_size = int(height * 0.8)
            else:
                font_size = self.font_size if self.font_size is not None else int(height * 0.8)

            def load_font(size: int) -> ImageFont.FreeTypeFont:
                return ImageFont.truetype(self.font, size)

            can_resize = True
        elif hasattr(self.font, "font_variant") and getattr(self.font, "size", None):
            font_size = int(height * 0.8) if self.auto_size else int(self.font.size)

            def load_font(size: int) -> ImageFont.FreeTypeFont:
                return self.font.font_variant(size=size)

            can_resize = True
        else:
            # Bitmap font or anything not scalable: use as-is.
            font_size = getattr(self.font, "size", None)
            can_resize = False

        font = load_font(font_size) if can_resize else self.font

        # Measure text size
        temp_img = Image.new("RGB", (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), self.text, font=font)
        text_width = bbox[2] - bbox[0]

        padding = 10

        if self.fixed_width_mm is not None:
            # Lock the label to exactly this width; shrink the font to fit
            # instead of expanding the label to the text.
            image_width = int(self.fixed_width_mm * resolution_dpi / 25.4)
            available = image_width - 2 * padding
            if available > 0 and text_width > available and can_resize and font_size:
                new_size = max(1, int(font_size * available / text_width))
                font = load_font(new_size)
                bbox = temp_draw.textbbox((0, 0), self.text, font=font)
                text_width = bbox[2] - bbox[0]
        else:
            # Create image sized to content with padding.
            image_width = int(text_width + 2 * padding)

            # Apply minimum width if specified
            if self.min_width_mm is not None:
                min_width_px = int(self.min_width_mm * resolution_dpi / 25.4)
                image_width = max(image_width, min_width_px)

        image = Image.new("RGB", (image_width, height), (255, 255, 255))

        draw = ImageDraw.Draw(image)

        # Horizontal alignment (account for bbox offset)
        if TextLabel.Align.LEFT in self.align:
            text_x = padding - bbox[0]
        elif TextLabel.Align.RIGHT in self.align:
            text_x = image_width - padding - bbox[2]
        else:  # HCENTER (default)
            text_x = (image_width - bbox[0] - bbox[2]) // 2

        # Vertical alignment (account for bbox offset)
        if TextLabel.Align.TOP in self.align:
            text_y = -bbox[1]
        elif TextLabel.Align.BOTTOM in self.align:
            text_y = height - bbox[3]
        else:  # VCENTER (default)
            text_y = (height - bbox[1] - bbox[3]) // 2

        draw.text((text_x, text_y), self.text, font=font, fill=(0, 0, 0))

        self._image = image


# Backwards compatibility alias
Align = TextLabel.Align
