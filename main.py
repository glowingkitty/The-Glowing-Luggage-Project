from machine import Pin
from neopixel import NeoPixel
import math
import time

red = (228, 0, 7)
blue = (0, 48, 228)
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
    elif brightness >= 0.7:
        direction = 'down'

    return brightness, direction


class LEDStrip():
    def __init__(self, brightness=0.3):
        self.stripSize = 30
        self.left = NeoPixel(Pin(17, Pin.OUT), self.stripSize, bpp=3)
        self.right = NeoPixel(Pin(18, Pin.OUT), self.stripSize, bpp=3)
        self.bottom = NeoPixel(Pin(5, Pin.OUT), self.stripSize, bpp=3)
        self.brightness = brightness
        self.time = 0.0

    def hall_sensor(self):
        import esp32

        value = 0
        while True:
            new_value = esp32.hall_sensor()
            if new_value != value:
                print(new_value)

            value = new_value
            time.sleep(0.1)

    def raw_temperature(self):
        import esp32

        value = 0
        while True:
            new_value = esp32.raw_temperature()
            if new_value != value:
                print(new_value)

            value = new_value
            time.sleep(0.1)

    def show_wifis(self):
        import network

        networks = []
        network_names = []

        wlan = network.WLAN(network.STA_IF)  # create station interface
        wlan.active(True)       # activate the interface

        while True:
            wifis = wlan.scan()
            for network in wifis:
                if network[0] not in network_names:
                    networks.append(network)
                    network_names.append(network[0])
                    print(network[0])

            time.sleep(0.1)

    def save_wifis(self, repeat=True):
        import network

        networks = []
        network_names = []

        wlan = network.WLAN(network.STA_IF)  # create station interface
        wlan.active(True)       # activate the interface

        if repeat:
            while True:
                wifis = wlan.scan()
                for network in wifis:
                    if network[0] not in network_names:
                        networks.append(network)
                        network_names.append(network[0])
                        print(network[0])
        else:
            wifis = wlan.scan()
            for network in wifis:
                if network[0] not in network_names:
                    networks.append(network)
                    network_names.append(network[0])
                    print(network[0])

    def light_off(self):
        for i in range(self.stripSize):
            self.bottom[i] = black
            self.right[i] = black
            self.left[i] = black

        self.right.write()
        self.left.write()
        self.bottom.write()

    def rainbow_animation(self, brightness=None, up_and_down=False):
        if not brightness:
            brightness = self.brightness
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

    def police_animation(self, brightness=None):
        if not brightness:
            brightness = 1

        LEDs_last = None

        while True:
            # red and blue on separate sides
            if LEDs_last == 'red':
                for i in range(self.stripSize):
                    self.right[i] = blue
                    self.left[i] = black
                LEDs_last = 'blue'

            else:
                for i in range(self.stripSize):
                    self.right[i] = black
                    self.left[i] = red
                LEDs_last = 'red'

            self.right.write()
            self.left.write()

            time.sleep(0.5)

    def arrows_forward(self, color='red', scan_wifis=True):
        # get base color
        if color == 'red':
            color = red

        reduce_factor = 0.4

        # create array of leds with decreasing brightness
        led_arrow = [color]
        while len(led_arrow) <= 5:
            led_arrow.insert(0, (
                round(led_arrow[0][0]*reduce_factor),
                round(led_arrow[0][1]*reduce_factor),
                round(led_arrow[0][2]*reduce_factor)
            ))

        # move array of leds over led strips
        position = self.stripSize-1
        while True:
            original_position = position

            # leds of led_arrow
            processed_leds = 0
            while processed_leds < len(led_arrow) and position >= 0:
                if position == -1:
                    position = len(led_arrow)
                self.right[position] = led_arrow[processed_leds]
                self.left[position] = led_arrow[processed_leds]

                position -= 1
                processed_leds += 1

            position = original_position

            for i in range(self.stripSize):
                if i > position or i < position-len(led_arrow):
                    self.right[i] = black
                    self.left[i] = black

                # light up bottom LEDs as well
                if position == 17:
                    self.bottom[i] = (
                        round(red[0]*0.3),
                        round(red[1]*0.3),
                        round(red[2]*0.3)
                    )
                elif position == 18:
                    self.bottom[i] = (
                        round(red[0]),
                        round(red[1]),
                        round(red[2])
                    )
                elif position == 19:
                    self.bottom[i] = (
                        round(red[0]*0.3),
                        round(red[1]*0.3),
                        round(red[2]*0.3)
                    )
                else:
                    # or make sure bottom LEDs are dark
                    self.bottom[i] = black

            self.right.write()
            self.left.write()
            self.bottom.write()

            time.sleep(1.0/30.0)
            position -= 1

            if position == -1:
                position = self.stripSize-1

    def test_leds(self):
        for i in range(self.stripSize):
            print('LED No. '+str(i))
            for e in range(self.stripSize):
                self.right[e] = black
                self.left[e] = black
                self.bottom[e] = black

            self.bottom[i] = red
            self.right[i] = red
            self.left[i] = red

            self.right.write()
            self.left.write()
            self.bottom.write()
            time.sleep(0.5)

    def music_animation(self):
        print()


LEDStrip().rainbow_animation(up_and_down=True)
# LEDStrip().police_animation()
# LEDStrip().light_off()
# LEDStrip().arrows_forward()
# LEDStrip().test_leds()
