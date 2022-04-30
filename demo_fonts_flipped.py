"""SSD1351 demo (fonts)."""
from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont


def test():
    """Test code."""
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))

    display.clear()

    print("Loading font, please wait.")
    arcadepix = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
    print("Font loaded.")

    # Portrait
    w=arcadepix.measure_text('Portrait')  # Measure length of text in pixels
    center = int(display.width / 2 - w / 2)  # Calculate position for centered text
    display.draw_text(center, display.height - arcadepix.height, 'Portrait', arcadepix, color565(0, 255, 0))
    sleep(1)

    # Portrait flipped upside down
    w = arcadepix.measure_text('Flipped')
    display.draw_text(display.width - w, 0, 'Flipped', arcadepix, color565(0, 255, 255),flip=True)
    sleep(1)

    # Landscape
    w = arcadepix.measure_text('Landscape')
    display.draw_text(display.height - arcadepix.height, display.width - w, 'Landscape', arcadepix,
                      color565(255, 255, 0), landscape=True)
    sleep(1)

    # Landscape flipped upside down
    display.draw_text(0, 0, 'Flipped Landscape', arcadepix, color565(255, 0, 255),landscape=True, flip=True)

    sleep(9)
    display.cleanup()


test()
