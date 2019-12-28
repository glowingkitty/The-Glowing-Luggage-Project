from machine import Pin
from neopixel import NeoPixel
import math
import time

stripSize = 30
LEDsBottom = NeoPixel(Pin(5, Pin.OUT), stripSize, bpp=3)
LEDsRight = NeoPixel(Pin(18, Pin.OUT), stripSize, bpp=3)
LEDsLeft = NeoPixel(Pin(17, Pin.OUT), stripSize, bpp=3)


def rainbow(t, i):
    a = (0.5, 0.5, 0.5)
    b = (0.5, 0.5, 0.5)
    c = (1.0, 1.0, 1.0)
    d = (0.00, 0.33, 0.67)

    k = t + 0.05 * i

    r = a[0] + b[0] * math.cos(6.28318 * (c[0] * k + d[0]))
    g = a[1] + b[1] * math.cos(6.28318 * (c[1] * k + d[1]))
    b = a[2] + b[2] * math.cos(6.28318 * (c[2] * k + d[2]))

    return (int(255.0 * r), int(255.0 * g), int(255.0 * b))


def render():

    t = 0.0

    while True:
        t += 0.06
        for i in range(stripSize):
            color = rainbow(t, i)
            LEDsBottom[i] = color
            LEDsRight[i] = color
            LEDsLeft[i] = color

        LEDsBottom.write()
        LEDsRight.write()
        LEDsLeft.write()

        time.sleep(1.0/36.0)


render()
