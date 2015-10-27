#Read a value from analogue input 0
#in A/D in the PCF8591P @ address 0x48
from smbus import  SMBus
import time

#bus = SMBus(0)
bus = SMBus(1)

print("Read the A/D")
print("Ctrl C to stop")
 
while True:
    print "--------"
    time.sleep(2)
    bus.write_byte(0x48, 0x40) # set control register to read channel 0
    reading0 = bus.read_byte(0x48) # read A/D
    print("0: ", reading0)

