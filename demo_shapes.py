"""SSD1351 demo (shapes)."""
from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI  # type: ignore


def test():
    """Test code."""
    # Baud rate of 14500000 seems about the max
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))

    display.clear(color565(64, 0, 255))
    sleep(1)

    display.clear()

    display.draw_hline(10, 127, 63, color565(255, 0, 255))
    sleep(1)

    display.draw_vline(10, 0, 127, color565(0, 255, 255))
    sleep(1)

    display.fill_hrect(23, 50, 30, 75, color565(255, 255, 255))
    sleep(1)

    display.draw_hline(0, 0, 127, color565(255, 0, 0))
    sleep(1)

    display.draw_line(127, 0, 64, 127, color565(255, 255, 0))
    sleep(2)

    display.clear()

    coords = [[0, 63], [78, 80], [122, 92], [50, 50], [78, 15], [0, 63]]
    display.draw_lines(coords, color565(0, 255, 255))
    sleep(1)

    display.clear()
    display.fill_polygon(7, 63, 63, 50, color565(0, 255, 0))
    sleep(1)

    display.fill_rectangle(0, 0, 15, 127, color565(255, 0, 0))
    sleep(1)

    display.clear()

    display.fill_rectangle(0, 0, 63, 63, color565(128, 128, 255))
    sleep(1)

    display.draw_rectangle(0, 64, 63, 63, color565(255, 0, 255))
    sleep(1)

    display.fill_rectangle(64, 0, 63, 63, color565(128, 0, 255))
    sleep(1)

    display.draw_polygon(3, 96, 96, 30, color565(0, 64, 255),
                         rotate=15)
    sleep(3)

    display.clear()

    display.fill_circle(32, 32, 30, color565(0, 255, 0))
    sleep(1)

    display.draw_circle(32, 96, 30, color565(0, 0, 255))
    sleep(1)

    display.fill_ellipse(96, 32, 30, 16, color565(255, 0, 0))
    sleep(1)

    display.draw_ellipse(96, 96, 16, 30, color565(255, 255, 0))

    sleep(5)
    display.cleanup()


test()
