from machine import Pin
from neopixel import NeoPixel
import math
import time

red = (237, 29, 35)
blue = (0, 31, 215)
black = (0, 0, 0)


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
        brightness = brightness + 0.025
    else:
        brightness = brightness - 0.025

    if brightness <= 0.1:
        direction = 'up'
    elif brightness >= 1:
        direction = 'down'

    return brightness, direction


class LED():
    def __init__(self, brightness=0.3):
        self.stripSize = 30
        self.left = NeoPixel(Pin(17, Pin.OUT), stripSize, bpp=3)
        self.right = NeoPixel(Pin(18, Pin.OUT), stripSize, bpp=3)
        self.bottom = NeoPixel(Pin(5, Pin.OUT), stripSize, bpp=3)
        self.brightness = brightness
        self.time = 0.0

    def rainbow_animation(self, brightness=self.brightness, up_and_down=False):
        if up_and_down:
            brightness, direction = change_brightness(0.1, 'up')

        while True:
            self.time += 0.06
            for i in range(self.stripSize):
                color = rainbow(self.time, i, brightness)
                self.bottom[i] = color
                self.right[i] = color
                self.left[i] = color

            self.bottom.write()
            self.right.write()
            self.left.write()

            if up_and_down:
                brightness, direction = change_brightness(
                    brightness, direction)

            time.sleep(1.0/36.0)

    def police_animation(self, brightness=self.brightness, mode='switch'):
        LEDs_last = None

        while True:
            if mode == 'switch':
                # switching between red and blue
                for i in range(self.stripSize):
                    if LEDs_last == 'red,blue':
                        self.right[i] = blue
                        self.left[i] = red
                        LEDs_last = 'blue,red'
                    else:
                        self.right[i] = red
                        self.left[i] = blue
                        LEDs_last = 'red,blue'

            elif mode == 'separate':
                # red and blue on separate sides
                for i in range(self.stripSize):
                    if LEDs_last == 'red':
                        self.right[i] = blue
                        self.left[i] = black
                        LEDs_last = 'blue'
                    else:
                        self.right[i] = black
                        self.left[i] = red
                        LEDs_last = 'red'

            self.right.write()
            self.left.write()

            time.sleep(1.0/36.0)

    def arrows_forward(self, brightness=self.brightness, color='red'):
        # get base color
        if color == 'red':
            color = (237, 29, 35)

        reduce_factor = 0.3

        # create array of leds with decreasing brightness
        led_arrow = [color]
        steps = 1
        while steps < 5:
            led_arrow.append((
                color[0]*reduce_factor,
                color[1]*reduce_factor,
                color[2]*reduce_factor
            ))
            steps += 1

        # move array of leds over led strips
        position = 0
        while True:

            # leds of led_arrow
            processed_leds = 0
            while processed_leds < len(self.led_arrow) and position >= 0:
                self.right[position] = led_arrow[processed_leds]
                self.left[position] = led_arrow[processed_leds]

                position -= 1
                processed_leds += 1

            position = processed_leds

            for i in range(self.stripSize):
                if i >= position:
                    self.right[i] = black
                    self.left[i] = black

            self.right.write()
            self.left.write()

            time.sleep(1.0/36.0)
            position += 1


LED().rainbow_animation(up_and_down=True)
# LED().police_animation(mode='separate')
