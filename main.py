from machine import Pin
from neopixel import NeoPixel
import math
import time

stripSize = 30
LEDsBottom = NeoPixel(Pin(5, Pin.OUT), stripSize, bpp=3)
LEDsRight = NeoPixel(Pin(18, Pin.OUT), stripSize, bpp=3)
LEDsLeft = NeoPixel(Pin(17, Pin.OUT), stripSize, bpp=3)


def rainbow(t, i, brightness):
    a = (0.5, 0.5, 0.5)
    b = (0.5, 0.5, 0.5)
    c = (1.0, 1.0, 1.0)
    d = (0.00, 0.33, 0.67)

    k = t + 0.05 * i

    r = a[0] + b[0] * math.cos(6.28318 * (c[0] * k + d[0]))
    g = a[1] + b[1] * math.cos(6.28318 * (c[1] * k + d[1]))
    b = a[2] + b[2] * math.cos(6.28318 * (c[2] * k + d[2]))

    return (int(255.0 * r * brightness), int(255.0 * g * brightness), int(255.0 * b * brightness))


def change_brightness(brightness, direction):
    if direction == 'up':
        brightness = brightness + 0.05
    else:
        brightness = brightness - 0.05

    if brightness <= 0.1:
        direction = 'up'
    elif brightness >= 1:
        direction = 'down'

    return brightness, direction


def rainbow_animation(brightness=0.3, up_and_down=False):

    t = 0.0

    if up_and_down:
        brightness, direction = change_brightness(0.1, 'up')

    while True:
        t += 0.06
        for i in range(stripSize):
            color = rainbow(t, i, brightness)
            LEDsBottom[i] = color
            LEDsRight[i] = color
            LEDsLeft[i] = color

        LEDsBottom.write()
        LEDsRight.write()
        LEDsLeft.write()

        if up_and_down:
            brightness, direction = change_brightness(brightness, direction)

        time.sleep(1.0/36.0)


rainbow_animation(up_and_down=True)
