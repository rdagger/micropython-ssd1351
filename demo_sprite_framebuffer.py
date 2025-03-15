"""SSD1351 demo (sprite framebuffer).

Notes: Will likely require device with PSRAM.
"""
from framebuf import FrameBuffer, RGB565  # type: ignore
from machine import Pin, SPI  # type: ignore
from ssd1351 import Display, color565
from struct import pack, unpack
from utime import sleep_us, ticks_us, ticks_diff  # type: ignore


class SpriteFrameBuffer(object):
    """Sprite Frame Buffer."""

    def __init__(self, sprite_path, background_image,
                 w, h, speed, display):
        """Initialize sprite.

        Args:
            sprite_path (string): Path of sprite image.
            background_image (string): Path of background image.
            w, h (int): Width and height of sprite.
            speed(int): Initial XY-Speed of sprite.
            display (SSD1351): OLED display object.
        """
        self.w = w
        self.h = h
        self.x_speed = speed
        self.y_speed = speed
        self.display = display
        self.screen_width = display.width
        self.screen_height = display.height
        self.x = 0  # Starting X coordinate
        self.y = self.screen_height // 4  # Starting Y coordinate
        # Set up back buffer
        back_buffer = bytearray(self.screen_width * self.screen_height * 2)
        # Create frame buffer for back buffer
        self.back_buffer_fb = FrameBuffer(back_buffer, self.screen_width,
                                          self.screen_height, RGB565)
        # Load background and convert to bytearray for framebuf compatiblility
        background = bytearray(
            display.load_sprite(background_image, self.screen_width,
                                self.screen_height))
        # Create frame buffer for background
        self.background_fb = FrameBuffer(background, self.screen_width,
                                         self.screen_height, RGB565)
        # Load sprite & convert to bytearray for framebuf compatibility
        sprite = bytearray(
            display.load_sprite(sprite_path, self.w, self.h))
        # Create frame buffer for foreground sprite
        self.sprite_fb = FrameBuffer(sprite, self.w, self.h, RGB565)

        # Need to swap endian for the key color
        self.key = unpack('>H', pack('<H', color565(0, 255, 0)))[0]

    def update_pos(self):
        """Update sprite speed and position."""
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        x_speed = abs(self.x_speed)
        y_speed = abs(self.y_speed)

        if x + w + x_speed >= self.screen_width:
            self.x_speed = -x_speed
        elif x - x_speed < 0:
            self.x_speed = x_speed

        if y + h + y_speed >= self.screen_height:
            self.y_speed = -y_speed
        elif y - y_speed <= 0:
            self.y_speed = y_speed

        self.x = x + self.x_speed
        self.y = y + self.y_speed

    def draw(self):
        """Draw sprite."""
        # Draw background to back buffer
        self.back_buffer_fb.blit(self.background_fb, 0, 0)
        # Draw sprite to back buffer
        self.back_buffer_fb.blit(self.sprite_fb, self.x, self.y, self.key)
        # Draw back buffer to display
        self.display.draw_sprite(self.back_buffer_fb, 0, 0,
                                 self.screen_width, self.screen_height)


def test():
    """Bouncing sprite."""
    try:
        # Baud rate of 14500000 seems about the max
        # spi = SPI(2, baudrate=14500000, sck=Pin(18), mosi=Pin(23))
        spi = SPI(1, baudrate=14500000, sck=Pin(12), mosi=Pin(11))
        display = Display(spi, dc=Pin(17), cs=Pin(5), rst=Pin(16))
        display.contrast(15)  # Set maximum brightness

        # Load sprite
        logo = SpriteFrameBuffer('images/Ostrich65x64.raw',
                                 'images/XP_background128x128.raw',
                                 65, 64, 1, display)

        while True:
            timer = ticks_us()
            logo.update_pos()
            logo.draw()
            # Attempt to set framerate to 30 FPS
            timer_dif = 33333 - ticks_diff(ticks_us(), timer)
            if timer_dif > 0:
                sleep_us(timer_dif)

    except KeyboardInterrupt:
        display.cleanup()


test()
