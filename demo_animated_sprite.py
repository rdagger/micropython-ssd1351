"""SSD1351 demo (animated sprite).

Notes: May require device with PSRAM
"""
from ssd1351 import Display
from machine import Pin, SPI  # type: ignore
from micropython import const  # type: ignore
from utime import sleep_us, ticks_us, ticks_diff  # type: ignore

SPRITE_WIDTH = const(65)
SPRITE_HEIGHT = const(64)
SPRITE_COUNT = const(8)
SIZE = const(8320)  # width (65) x height (64) x bytes of color (2)


def test():
    """Test code."""
    try:
        # Baud rate of 40000000 seems about the max
        spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
        # display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))
        display = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(15))
        display.clear()

        # Load sprite
        ostrich = display.load_sprite('images/Ostrich65x512.raw',
                                      SPRITE_WIDTH,
                                      SPRITE_HEIGHT * SPRITE_COUNT)
        # Use memoryview to improve memory usage
        mv_ostrich = memoryview(ostrich)

        x = (display.width - SPRITE_WIDTH) // 2
        y = (display.height - SPRITE_HEIGHT) // 2
        index = 0  # Sprite frame index

        while True:
            timer = ticks_us()
            offset = SIZE * index
            display.draw_sprite(mv_ostrich[offset: offset + SIZE], x, y,
                                SPRITE_WIDTH, SPRITE_HEIGHT)
            index = (index + 1) & 7  # Next sprite index (wrap on last)

            # Attempt to set framerate to 30 FPS
            timer_dif = 33333 - ticks_diff(ticks_us(), timer)
            if timer_dif > 0:
                sleep_us(timer_dif)

    except KeyboardInterrupt:
        display.cleanup()


test()
