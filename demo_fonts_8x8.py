"""SSD1351 demo (fonts 8x8)."""
from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI


def test():
    """Test code."""
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))

    display.draw_text8x8(0, 0, 'Built-in', color565(255, 0, 255))
    display.draw_text8x8(16, 16, 'MicroPython', color565(255, 255, 0))
    display.draw_text8x8(32, 32, '8x8 Font', color565(0, 0, 255))
    display.draw_text8x8(63, 120, "Portrait", color565(0, 255, 0))
    display.draw_text8x8(0, 56, "Landscape", color565(255, 0, 0),
                         landscape=True)

    sleep(9)
    display.cleanup()


test()
