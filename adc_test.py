from smbus import  SMBus
import time

# Read a value from analogue input 0
# in A/D in the PCF8591P @ address 0x48
# On the PiA, the pin2,3 i2c is on bus(1)
def read_adc0_mv():
  bus = SMBus(1)
  time.sleep(1) # settle
  bus.write_byte(0x48, 0x40) # set control register to read channel 0
  value = bus.read_byte(0x48)
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

millivolts = read_adc0_mv()
millivolts = read_adc0_mv()

while True:
  millivolts = read_adc0_mv()
  print "ADC0 voltage is ", millivolts / 1000.0
  print "Equivalent UV rating is ", mv_to_uvrating(millivolts)
  time.sleep(1)

