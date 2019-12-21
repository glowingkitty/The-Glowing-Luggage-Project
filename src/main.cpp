#include <Arduino.h>
#include <FastLED.h>

//#define STRIPTYPE NEOPIXEL

const int stripSize = 30;
const int hueStep = 8;
const int segmentSize = 10;
const int showFrom = 0;
constexpr uint8_t stripPinTop = 18;
constexpr uint8_t stripPinBottom = 17;

CRGB colorsTop[stripSize];
CRGB colorsBottom[stripSize];
int initialHue = 0;
void setup()
{
  // put your setup code here, to run once:
  FastLED.addLeds<NEOPIXEL, stripPinTop>(colorsTop, int(stripSize));
  FastLED.addLeds<NEOPIXEL, stripPinBottom>(colorsBottom, int(stripSize));
}

void hueShift()
{
  initialHue += 10;
}

int segmentStart = segmentSize - 1;
void segmentShift()
{
  segmentStart--;
  if (segmentStart < 0)
  {
    segmentStart = segmentSize - 1;
  }
}

void loop()
{

  for (int k = 0; k < 5; k++)
  {
    int hue = initialHue;
    for (int i = 0; i < stripSize; i++, hue += hueStep)
    {
      if ((i + segmentStart) % segmentSize < showFrom)
      {
        colorsTop[i] = CRGB::Black;
        colorsBottom[i] = CRGB::Black;
      }
      else
      {
        colorsTop[i] = CHSV(hue % 256, 255, 255);
        colorsBottom[i] = CHSV(hue % 140, 255, 255);
      }
    }
    FastLED.show(100);
    delay(50);
    hueShift();
  }
  segmentShift();
}