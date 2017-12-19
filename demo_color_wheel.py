"""SSD1351 demo (color wheel)."""
from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI
from math import cos, pi, sin


def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB (based on colorsys.py).

        Args:
            h (float): Hue 0 to 1.
            s (float): Saturation 0 to 1.
            v (float): Value 0 to 1 (Brightness).
    """
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)

    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def test():
    """Test code."""
    # Baud rate of 14500000 seems about the max
    spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
    display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))

    x, y = 0, 0
    w, h = 128, 128
    length = 63
    angle = 0.0
    angle_step_size = 0.05  # Decrease step size for higher resolution

    #  Loop all angles from 0 to 2 * PI radians
    while angle < 2 * pi:
        # Calculate x, y from a vector with known length and angle
        x = length * sin(angle)
        y = length * cos(angle)
        x1 = int(x + w / 2)
        y1 = int(y + h / 2)
        color = color565(*hsv_to_rgb(angle / (2 * pi), 1, 1))
        display.draw_line(x1, y1, 63, 63, color)
        angle += angle_step_size

    sleep(5)
    display.clear()

    for r in range(1, 64):
        color = color565(*hsv_to_rgb(r / 64, 1, 1))
        display.draw_circle(63, 63, r, color)

    sleep(9)
    display.cleanup()


test()
