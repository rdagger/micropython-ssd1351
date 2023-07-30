"""SSD1351 demo (boundaries)."""
from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI

RED = const(0XF800)  # (255, 0, 0)
GREEN = const(0X07E0)  # (0, 255, 0)
WHITE = const(0XFFF)  # (255, 255, 255)


def test():
    """Test code."""
    # Baud rate of 14500000 seems about the max
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    print('spi started')
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))
    print('display started')

    w = display.width
    h = display.height

    display.clear()

    display.draw_rectangle(0, 0, w, h, RED)
    display.draw_pixel(0, 0, WHITE)
    display.draw_pixel(0, h - 1, WHITE)
    display.draw_pixel(w - 1, 0, WHITE)
    display.draw_pixel(w - 1, h - 1, WHITE)
    sleep(5)

    display.fill_rectangle(0, 0, w, h, GREEN)
    sleep(5)

    display.draw_rectangle(0, 0, w, h, RED)
    display.draw_pixel(0, 0, WHITE)
    display.draw_pixel(0, h - 1, WHITE)
    display.draw_pixel(w - 1, 0, WHITE)
    display.draw_pixel(w - 1, h - 1, WHITE)

    sleep(10)
    display.cleanup()


test()
