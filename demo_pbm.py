"""SSD1351 demo (PBM - Portable Bitmap).

This demo is based on code provided by MimiVRC
"""
from ssd1351 import Display, color565
from struct import pack, unpack
from framebuf import FrameBuffer, MONO_HLSB, RGB565  # type: ignore
from machine import Pin, SPI  # type: ignore
from time import sleep


def create_palette(foreground, background=0, invert=False):
    """Create framebuffer palette to translate between MONO_HLSB and RGB565.

    Args:
        foreground(int): Foreground color in RGB656 format
        background(int): Background color in RGB656 format (Default Black)
        invert(bool): Invert foreground and background (default False)
    Returns:
            FrameBuffer: Color palette
    """
    # Need to swap endian colors
    foreground = unpack('>H', pack('<H', foreground))[0]
    background = unpack('>H', pack('<H', background))[0]

    # Buffer size equals 2 pixels (MONO_HLSB) x 2 byte color depth (RGB565)
    buffer_size = 4
    # Define framebuffer
    palette = FrameBuffer(bytearray(buffer_size), 2, 1, RGB565)
    # Set foreground & background color pixels (swap if inverted)
    palette.pixel(0 if invert else 1, 0, background)
    palette.pixel(1 if invert else 0, 0, foreground)
    return palette


def load_pbm(filename):
    """Load portable bitmap file.

    Args:
        filename(str): Path to bitmap
    Returns:
            FrameBuffer: Image in MONO_HLSB format
    """
    with open(filename, 'rb') as f:
        # Read and discard the first 2 lines
        for _ in range(2):
            f.readline()
        # Read dimensions from the third line
        dimensions = f.readline().split()
        width = int(dimensions[0])
        height = int(dimensions[1])

        # Read the bitmap data
        data = bytearray(f.read())
    return FrameBuffer(data, width, height, MONO_HLSB), width, height


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))
    display.clear()

    # Define palettes
    red = create_palette(color565(255, 0, 0))
    magenta = create_palette(color565(255, 0, 255))
    green = create_palette(color565(0, 255, 0), invert=True)
    blue = create_palette(color565(0, 0, 255), invert=True)
    yellow = create_palette(color565(255, 255, 0),
                            background=color565(0, 0, 255),
                            invert=True)
    white = create_palette(color565(255, 255, 255),
                           background=color565(0, 255, 255))

    # Load invader .PBM image to framebuffer and get dimensions
    invader_fb, w, h = load_pbm('images/invaders48x36.pbm')

    # Create RGB565 placeholder
    placeholder = bytearray(w * h * 2)
    # Create frame buffer for placeholder
    placeholder_fb = FrameBuffer(placeholder, w, h, RGB565)

    # Draw 6 invaders in different color palettes
    placeholder_fb.blit(invader_fb, 0, 0, -1, red)
    display.draw_sprite(placeholder, 0, 0, w, h)

    placeholder_fb.blit(invader_fb, 0, 0, -1, magenta)
    display.draw_sprite(placeholder, display.width - w, 0, w, h)

    placeholder_fb.blit(invader_fb, 0, 0, -1, green)
    display.draw_sprite(placeholder, 0,
                        (display.height - h) // 2, w, h)

    placeholder_fb.blit(invader_fb, 0, 0, -1, blue)
    display.draw_sprite(placeholder, display.width - w,
                        (display.height - h) // 2, w, h)

    placeholder_fb.blit(invader_fb, 0, 0, -1, yellow)
    display.draw_sprite(placeholder, 0, display.height - h, w, h)

    placeholder_fb.blit(invader_fb, 0, 0, -1, white)
    display.draw_sprite(placeholder, display.width - w,
                        display.height - h, w, h)
    sleep(10)

    display.cleanup()


test()
