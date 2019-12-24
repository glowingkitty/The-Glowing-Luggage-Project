from machine import Pin
from neopixel import NeoPixel
import math
import time

stripSize = 30
LEDsTop = NeoPixel(Pin(18, Pin.OUT), stripSize, bpp=3)
LEDsBottom = NeoPixel(Pin(17, Pin.OUT), stripSize, bpp=3)


def smooth_colors(t, i):
    offset = float(i) / 30.0 * math.pi

    r = 0.5 + 0.5 * math.cos(2.0 * t + 2.0 + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * t + 3.0 + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * t + 4.0 + offset)

    return (int(255.0 * r), int(255.0 * g), int(255.0 * b))


# vec3 palette( in float t, in vec3 a, in vec3 b, in vec3 c, in vec3 d )
#  return a + b*cos( 6.28318*(c*t+d) );

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
            LEDsTop[i] = color
            LEDsBottom[i] = color

        LEDsBottom.write()
        LEDsTop.write()

        time.sleep(1.0/36.0)


render()
