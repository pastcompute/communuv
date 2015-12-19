from time import sleep
from subprocess import call
from random import randint

fake = False
try:
  from smbus import  SMBus
  import RPi.GPIO as GPIO
except:
  fake = True

testmode = 0
# do env now
#testmode = 9


I2C_PCF8591 = 0x48
RPI_GPIO_I2C_BUS = 1

LED_EXTREME = 17
LED_VERYHIGH = 27
LED_HIGH = 22
LED_MEDIUM = 18
LED_LOW = 23

GP_SWITCH = 24

def setup_hardware():
  if fake:
    print "Fake mode: skipping GPIO init"
    return
  GPIO.setmode(GPIO.BCM)

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
  if fake: return randint(0, 2450)

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
  print "set all LEDs"
  if fake: return
  GPIO.output(LED_LOW, GPIO.HIGH);
  GPIO.output(LED_MEDIUM, GPIO.HIGH);
  GPIO.output(LED_HIGH, GPIO.HIGH);
  GPIO.output(LED_VERYHIGH, GPIO.HIGH);
  GPIO.output(LED_EXTREME, GPIO.HIGH);

def clear_leds():
  print "clear all LEDs"
  if fake: return
  GPIO.output(LED_LOW, GPIO.LOW);
  GPIO.output(LED_MEDIUM, GPIO.LOW);
  GPIO.output(LED_HIGH, GPIO.LOW);
  GPIO.output(LED_VERYHIGH, GPIO.LOW);
  GPIO.output(LED_EXTREME, GPIO.LOW);

def cycle_through_leds():
  print "cycle through LEDs"
  if fake: return
  clear_leds()
  GPIO.output(LED_LOW, GPIO.HIGH);
  sleep(0.35)
  GPIO.output(LED_LOW, GPIO.LOW);
  sleep(0.15)
  GPIO.output(LED_MEDIUM, GPIO.HIGH);
  sleep(0.35)
  GPIO.output(LED_MEDIUM, GPIO.LOW);
  sleep(0.15)
  GPIO.output(LED_HIGH, GPIO.HIGH);
  sleep(0.35)
  GPIO.output(LED_HIGH, GPIO.LOW);
  sleep(0.15)
  GPIO.output(LED_VERYHIGH, GPIO.HIGH);
  sleep(0.35)
  GPIO.output(LED_VERYHIGH, GPIO.LOW);
  sleep(0.15)
  GPIO.output(LED_EXTREME, GPIO.HIGH);
  sleep(0.35)
  GPIO.output(LED_EXTREME, GPIO.LOW);
  sleep(0.15)
  clear_leds()

def boot_leds():
  print "boot LEDs"
  if fake: return
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
  print "button pressed LEDs"
  if fake: return
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
  sleep(0.15)
  GPIO.output(LED_MEDIUM, GPIO.HIGH);
  sleep(0.15)
  GPIO.output(LED_HIGH, GPIO.HIGH);
  sleep(0.15)
  GPIO.output(LED_VERYHIGH, GPIO.HIGH);
  sleep(0.15)
  GPIO.output(LED_EXTREME, GPIO.HIGH);
  sleep(0.15)
  clear_leds()
  sleep(0.15)
  all_leds()
  sleep(0.15)
  GPIO.output(LED_EXTREME, GPIO.LOW);
  sleep(0.15)
  GPIO.output(LED_VERYHIGH, GPIO.LOW);
  sleep(0.15)
  GPIO.output(LED_HIGH, GPIO.LOW);
  sleep(0.15)
  GPIO.output(LED_MEDIUM, GPIO.LOW);
  sleep(0.15)
  GPIO.output(LED_LOW, GPIO.LOW);

def rating_leds(rating):
  print "rating LEDs ", rating
  if fake: return
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
  speak("Thank you for helping the Commun UV poject", "Thanks.wav")
  speak("Info", "Info.wav")

def speak_random_fact():
  speak("did you know", "Didyouknow.wav")
  r = randint(0,2)  # number of facts
  if r==0:
    speak("fact1", "Fact1.wav")
  else:
    speak("fact2", "Fact2.wav")

  sleep(0.5)
  #speak("Christmas", "christmas2014.wav")

def speak_rating_only(rating):
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

def speak_rating(rating):

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

  # speak("This rating is ")

  if (rating < 3):
    speak("Low", "ratinglow.wav")
  elif (rating < 6):
    speak("Medium", "ratingmedium.wav")
  elif (rating < 9):
    speak("High. ", "ratinghigh.wav")
    speak("Slip slop slap. ", "high2.wav")
  elif (rating < 11 ):
    speak("Very High. You should be wearing sunscreen and staying hydrated", "ratingveryhigh.wav")
    speak("Slip slop slap. ", "high2.wav")
    speak("Drink water", "Hydrated.wav")
  else:
    speak("Extreme. If you are not wearing sunsceen you are now `being sunburned!", "ratingextreme.wav")
    speak("Stay inside. ", "Extreme2.wav")
    speak("Drink water", "Hydrated.wav")

  # FIXME speak("Hydrate", "Hydrated.wav")


def speak_website(millivolts, rating):
  if millivolts < 10:
    # Darkweb
    speak("Please visit h t t p : // commun-uv.weebly.com and learn about the CommonUV project")
    speak("You may like to try again in daylight, and help us by reporting the UV rating")
    speak("This will help us track localised UV radiation, which may differ from ")
    speak("The published Adelaide rating due to cloud cover, for example")  

    speak("Visit website", "DArkweb.wav")
    speak("web", "IntoOurWebsite.wav")
  else:
    #speak("Please visit h t t p : // commun-uv.weebly.com and enter the rating number")
    # FIXME Crowsdource.wav
    #speak("This will help us track localised UV radiation, which may differ from ")
    #speak("The published Adelaide rating due to cloud cover, for example")
    speak("Crowdsource", "Crowdsource.wav")
    speak("Please", "PleaseLogYourReading.wav")
    speak_rating_only(rating) 
    #speak("And this location, which is Tonsley")
    speak("web", "IntoOurWebsite.wav")

  #speak("More information is at h t t p : // commun-uv.weebly.com") # Info.wav

    cycle_through_leds()

    speak("web", "toodark2.wav")  # arpansa

    rating_leds(rating)


def speak_random_cancer_stats():
  speak("While we are waiting, did you know that on data.sa", "cancer1.wav")  # Cancer1.wav

  x = randint(0,4) + 2010
  if x == 2010:
    speak("2011", "2010.wav") 
    speak("(stats for year A)", "CancerA.wav")
  elif x == 2011:
    speak("2011", "2011.wav") 
    speak("(stats for year B)", "CancerB.wav")
  elif x == 2012:
    speak("2012", "2012.wav") 
    speak("(stats for year C)", "CancerC.wav")
  elif x == 2013:
    speak("2013", "2013.wav") 
    speak("(stats for year D)", "CancerD.wav")
  elif x == 2014:
    speak("2014", "2014.wav") 
    speak("(stats for year E)", "CancerE.wav")

  # Cancer2.wav
  speak("significant proportion caused by UV", "cancer2.wav")  # Cancer1.wav

  speak("in 1977 there were less", "CancerF.wav")

  # https://data.sa.gov.au/data/dataset/sa-cancer-registry/resource/e2925b74-6811-439f-9063-77bc00253ca9

  speak("gp", "GP+.wav")

  # Nearest treatment

  # https://data.sa.gov.au/data/dataset/6da4db36-e461-483c-9c3b-d21c48423d7e/resource/31f1d816-339d-44af-87c7-83b10e481f03/download/gpplus.zip

  # Wav: gplus 1 2 3

setup_hardware()

boot_leds()

millivolts = read_adc0_mv()
millivolts = read_adc0_mv()
millivolts = read_adc0_mv()

speak("Welcome to commun U V", "Welcome.wav")

print "ADC0 voltage is ", millivolts / 1000.0
print "Equivalent UV rating is ", mv_to_uvrating(millivolts)

while True:
  GPIO.output(LED_EXTREME, GPIO.HIGH);

  # TODO: how to background flash?

  if fake:
    sleep(5)
  else:
    GPIO.wait_for_edge(GP_SWITCH, GPIO.RISING)
    GPIO.wait_for_edge(GP_SWITCH, GPIO.FALLING)
  print "Someone pressed the button"

  all_leds()
  speak("Welcome to commun U V", "Welcome.wav")
  speak("Commun U V helps maintain comunity awaress about U V exposure and skin cancer", "Welcome2.wav")  # Welcome2
  button_leds()
  cycle_through_leds()
  all_leds()

  speak("I will now check the current U V radiation level", "Welcome3.wav")  # Welcome3

  speak_random_cancer_stats()

  millivolts = read_adc0_mv()
  rating = mv_to_uvrating(millivolts)
  if testmode > 0:
    millivolts = 324
    rating = testmode
  elif millivolts < 10:
    rating = 7 

  rating_leds(rating)

  if millivolts < 10:
    speak("It seems to be dark, or you are inside", "TooDarkTheMeasureWas.wav")
    # speak("(last years UV rating)")
    speak_rating(rating)
  else:
    speak("FIXME: Measure1: The current UV rating is", "TheMeasureIs.wav")  # Measure1.wav
    speak_rating(rating)

  speak_random_fact()

  speak_website(millivolts, rating)

  speak_thankyou() # and Info.wav


# Extra stuff
# On 1 nov 2014
# Arpansa data det
# Cancer data set

# ToDO on website:

# data.sa links
# ABS link for population  1976 http://abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/2104.01976?OpenDocument

