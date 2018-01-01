"""SSD1351 demo (contrast)."""
from time import sleep
from ssd1351 import color565, Display
from machine import Pin, SPI
from xglcd_font import XglcdFont


def test():
    """Test code."""
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))
    bally = XglcdFont('fonts/Bally7x9.c', 7, 9)
    contrast_range = list(range(1, 16)) + list(reversed(range(15)))
    for c in contrast_range:
        display.clear()
        display.contrast(c)
        display.draw_image('images/MicroPython128x128.raw', 0, 0, 128, 128)
        display.draw_text(30, 119, 'contrast: {0}'.format(c),
                          bally, color565(255, 255, 255))
        sleep(1)

    display.cleanup()


test()
