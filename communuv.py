from smbus import  SMBus
from time import sleep
from subprocess import call
from random import randint
import RPi.GPIO as GPIO

testmode = 0
# do env now
testmode = 9

GPIO.setmode(GPIO.BCM)

I2C_PCF8591 = 0x48
RPI_GPIO_I2C_BUS = 1

LED_EXTREME = 17
LED_VERYHIGH = 27
LED_HIGH = 22
LED_MEDIUM = 18
LED_LOW = 23

GP_SWITCH = 24

GPIO.setup(LED_LOW, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LED_HIGH, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LED_VERYHIGH, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LED_EXTREME, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LED_MEDIUM, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(GP_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Read a value from analogue input 0
# in A/D in the PCF8591P @ address 0x48
# On the PiA, the pin2,3 i2c is on bus(1)
def read_adc0_mv():
  bus = SMBus(RPI_GPIO_I2C_BUS)
  sleep(1) # settle
  bus.write_byte(I2C_PCF8591, 0x40) # set control register to read channel 0
  value = bus.read_byte(I2C_PCF8591)
  # Value is E 0..255 fractions of Vref, Vref = 2.5V
  return float(value) * 2500.0 / 255.0

def mv_to_uvrating(mv):
  if mv < 50: return 0
  if mv < 227: return 1
  if mv < 318: return 2
  if mv < 408: return 3
  if mv < 503: return 4
  if mv < 606: return 5
  if mv < 696: return 6
  if mv < 795: return 7
  if mv < 881: return 8
  if mv < 976: return 9
  if mv < 1079: return 10
  return 11 
  

def all_leds():
  GPIO.output(LED_LOW, GPIO.HIGH);
  GPIO.output(LED_MEDIUM, GPIO.HIGH);
  GPIO.output(LED_HIGH, GPIO.HIGH);
  GPIO.output(LED_VERYHIGH, GPIO.HIGH);
  GPIO.output(LED_EXTREME, GPIO.HIGH);

def clear_leds():
  GPIO.output(LED_LOW, GPIO.LOW);
  GPIO.output(LED_MEDIUM, GPIO.LOW);
  GPIO.output(LED_HIGH, GPIO.LOW);
  GPIO.output(LED_VERYHIGH, GPIO.LOW);
  GPIO.output(LED_EXTREME, GPIO.LOW);

def cycle_through_leds():
  clear_leds()
  GPIO.output(LED_LOW, GPIO.HIGH);
  sleep(0.75)
  GPIO.output(LED_LOW, GPIO.LOW);
  sleep(0.25)
  GPIO.output(LED_MEDIUM, GPIO.HIGH);
  sleep(0.75)
  GPIO.output(LED_MEDIUM, GPIO.LOW);
  sleep(0.25)
  GPIO.output(LED_HIGH, GPIO.HIGH);
  sleep(0.75)
  GPIO.output(LED_HIGH, GPIO.LOW);
  sleep(0.25)
  GPIO.output(LED_VERYHIGH, GPIO.HIGH);
  sleep(0.75)
  GPIO.output(LED_VERYHIGH, GPIO.LOW);
  sleep(0.25)
  GPIO.output(LED_EXTREME, GPIO.HIGH);
  sleep(0.75)
  GPIO.output(LED_EXTREME, GPIO.LOW);
  sleep(0.25)
  clear_leds()

def boot_leds():
  all_leds()
  sleep(1.5)
  clear_leds()
  sleep(1)
  all_leds()
  sleep(1.5)
  clear_leds()
  sleep(1)
  cycle_through_leds()
  sleep(1)

def button_leds():
  clear_leds()
  sleep(0.1)
  all_leds()
  sleep(0.25)
  clear_leds()
  sleep(0.25)
  all_leds()
  sleep(0.25)
  clear_leds()
  sleep(0.25)
  GPIO.output(LED_LOW, GPIO.HIGH);
  sleep(0.5)
  GPIO.output(LED_MEDIUM, GPIO.HIGH);
  sleep(0.5)
  GPIO.output(LED_HIGH, GPIO.HIGH);
  sleep(0.5)
  GPIO.output(LED_VERYHIGH, GPIO.HIGH);
  sleep(0.5)
  GPIO.output(LED_EXTREME, GPIO.HIGH);
  sleep(0.5)
  clear_leds()
  sleep(0.5)
  all_leds()
  sleep(0.5)
  GPIO.output(LED_EXTREME, GPIO.LOW);
  sleep(0.5)
  GPIO.output(LED_VERYHIGH, GPIO.LOW);
  sleep(0.5)
  GPIO.output(LED_HIGH, GPIO.LOW);
  sleep(0.5)
  GPIO.output(LED_MEDIUM, GPIO.LOW);
  sleep(0.5)
  GPIO.output(LED_LOW, GPIO.LOW);

def rating_leds(rating):
  clear_leds()
  GPIO.output(LED_LOW, GPIO.HIGH);
  if (rating > 2):
    GPIO.output(LED_MEDIUM, GPIO.HIGH);
  if (rating > 5):
    GPIO.output(LED_HIGH, GPIO.HIGH);
  if (rating > 8 ):
    GPIO.output(LED_VERYHIGH, GPIO.HIGH);
  if (rating > 10 ):
    GPIO.output(LED_EXTREME, GPIO.HIGH);

def speak(text, filename=""):
  print "[SPEAK] ", text
  if filename == "":
    pass
  else:
    call(['alsaplayer', filename])

def speak_thankyou():
  speak("Thank you for helping the Commun UV poject")

def speak_random_fact():
  speak("did you know", "Didyouknow.wav")
  r = randint(0,2)  # number of facts
  if r==0:
    speak("fact1", "Fact1.wav")
  else:
    speak("fact2", "Fact2.wav")

def speak_rating(rating):
  speak("The current UV rating is", "TheMeasureIs.wav")

  if (rating == 0): speak("zero")
  elif (rating == 1): speak("one", "1.wav")
  elif (rating == 2): speak("two", "2.wav")
  elif (rating == 3): speak("three", "3.wav")
  elif (rating == 4): speak("four", "4.wav")
  elif (rating == 5): speak("five", "5.wav")
  elif (rating == 6): speak("six", "6.wav")
  elif (rating == 7): speak("seven", "7.wav")
  elif (rating == 8): speak("eight", "8.wav")
  elif (rating == 9): speak("nine", "9.wav")
  elif (rating == 10): speak("ten", "10.wav")
  else: speak("eleven or above", "11.wav")

  speak("This rating is ")

  if (rating < 3):
    speak("Low")
  elif (rating < 6):
    speak("Medium")
  elif (rating < 9):
    speak("High. We recommend you aeweaing sunscreen")
  elif (rating < 11 ):
    speak("Very High. You should be wearing sunscreen and staying hydrated")
  else:
    speak("Extreme. If you are not wearing sunsceen you are now `being sunburned!")

def speak_website(millivolts, rating):
  if millivolts < 10:
    speak("Please visit h t t p : // commun-uv.weebly.com and learn about the CommonUV project")
    speak("You may like to try again in daylight, and help us by reporting the UV rating")
    speak("This will help us track localised UV radiation, which may differ from ")
    speak("The published Adelaide rating due to cloud cover, for example")  
  else:
    speak("Please visit h t t p : // commun-uv.weebly.com and enter the rating number")
    speak("Please", "PleaseLogYourReading.wav")
    speak_rating(rating) 
    speak("And this location, which is Tonsley")
    speak("web", "IntoOurWebsite.wav")
    speak("This will help us track localised UV radiation, which may differ from ")
    speak("The published Adelaide rating due to cloud cover, for example")
  speak("More information is at h t t p : // commun-uv.weebly.com")

boot_leds()

millivolts = read_adc0_mv()
millivolts = read_adc0_mv()
millivolts = read_adc0_mv()

print "ADC0 voltage is ", millivolts / 1000.0
print "Equivalent UV rating is ", mv_to_uvrating(millivolts)

while True:
  GPIO.wait_for_edge(GP_SWITCH, GPIO.RISING)
  GPIO.wait_for_edge(GP_SWITCH, GPIO.FALLING)
  print "Someone pressed the button"

  all_leds()
  speak("Welcome to commun U V", "Welcome.wav")
  speak("Commun U V helps maintain comunity awaress about U V exposure and skin cancer")
  button_leds()

  speak("I will now check the current U V radiation level")

  millivolts = read_adc0_mv()
  rating = mv_to_uvrating(millivolts)
  if testmode > 0:
    millivolts = 324
    rating = testmode
  if millivolts < 10:
    speak("It seems to be dark, or you are inside", "TooDarkTheMeasureWas.wav")
    speak("This time last year, the average UV rating was")
    speak("(last years UV rating)")
  else:
    speak_rating(rating)

  rating_leds(rating)

  speak_random_fact()

  speak_website(millivolts, rating)

  speak_thankyou()

# Extra stuff
# On 1 nov 2014
# Arpansa data det
# Cancer data set
