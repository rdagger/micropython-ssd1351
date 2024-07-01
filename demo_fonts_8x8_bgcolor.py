"""SSD1351 demo (fonts 8x8 background color)."""
from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI  # type: ignore


def test():
    """Test code."""
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))

    display.draw_text8x8(0, 0, 'Built-in', color565(255, 0, 0))
    display.fill_rectangle(0, 10, 95, 12, color565(255, 0, 0))
    display.draw_text8x8(0, 12, 'Built-in', color565(0, 0, 0),
                         color565(255, 0, 0))

    display.draw_text8x8(0, 28, 'MicroPython', color565(0, 255, 0))
    display.fill_rectangle(0, 38, 95, 12, color565(0, 255, 0))
    display.draw_text8x8(0, 40, 'MicroPython', color565(0, 0, 0),
                         color565(0, 255, 0))

    display.draw_text8x8(0, 56, '8x8 Font', color565(0, 0, 255))
    display.fill_rectangle(0, 66, 95, 12, color565(0, 0, 255))
    display.draw_text8x8(0, 68, '8x8 Font', color565(0, 0, 0),
                         color565(0, 0, 255))

    
    display.draw_text8x8(0, 105, 'No Background', color565(255, 255, 255))
    display.fill_rectangle(0, 115, 105, 12, color565(255, 255, 255))
    display.draw_text8x8(0, 117, 'No Background', color565(255, 255, 255))


    display.draw_text8x8(display.width - 29, 0, "Landscape",
                         color565(255, 255, 255), landscape=True)
    display.fill_rectangle(display.width - 19, 0, 18, 128,
                           color565(255, 128, 0))
    display.draw_text8x8(display.width - 14, 0, "Landscape",
                         color565(255, 255, 255),
                         background=color565(255, 128, 0),
                         landscape=True)

    sleep(15)
    display.cleanup()


test()
