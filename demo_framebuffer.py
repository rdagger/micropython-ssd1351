"""SSD1351 demo (framebuffer).

Notes: May require device with PSRAM
"""
from ssd1351 import Display, color565
from struct import pack, unpack
from framebuf import FrameBuffer, RGB565  # type: ignore
from machine import Pin, SPI  # type: ignore
from time import sleep


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))
    display.clear()

    # Load background and convert to bytearray for framebuf compatiblility
    background = bytearray(
        display.load_sprite('images/XP_background128x128.raw', 128, 128))
    # Create frame buffer for background
    background_fb = FrameBuffer(background, 128, 128, RGB565)

    # Load ostrich sprite and convert to bytearray for framebuf compatibility
    ostrich = bytearray(
        display.load_sprite('images/Ostrich65x64.raw', 65, 64))
    # Create frame buffer for foreground ostrich
    ostrich_fb = FrameBuffer(ostrich, 65, 64, RGB565)

    # Get X,Y coordinates to center ostrich on screen
    x = (display.width - 65) // 2
    y = (display.height - 64) // 2

    # Need to swap endian for the key color
    key = unpack('>H', pack('<H', color565(0, 255, 0)))[0]

    # Draw ostrich on background with transparent key
    background_fb.blit(ostrich_fb, x, y, key)

    # Draw background with ostrich on display
    display.draw_sprite(background, 0, 0, 128, 128)
    sleep(10)

    display.cleanup()


test()
