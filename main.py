import machine
import utime

sda=machine.Pin(0)
scl=machine.Pin(1)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)

led_onboard = machine.Pin(25, machine.Pin.OUT)

utime.sleep(1) # REQUIRED to allow the SerLCD to initialise, code will not run on boot without this delay

i2c.writeto(114, '\x7C') #enter settings mode
i2c.writeto(114, '\x18') #change contrast
i2c.writeto(114, '\xAA') #set contrast to 170/255

i2c.writeto(114, '\x7C') #enter settings mode
i2c.writeto(114, '\x2B') #change backlight RGB values
i2c.writeto(114, '\x00') #set red value to 170/255
i2c.writeto(114, '\xFF') #set green value to 170/255
i2c.writeto(114, '\x00') #set blue value to 170/255

i2c.writeto(114, '\x7C') #enter settings mode
i2c.writeto(114, '\x2D') #clear display

adc = machine.ADC(4) #setup analogue-to-digital converter on channel 4 for temperature sensor
conversion_factor = 3.3 / (65535) # convert raw value to voltage value

while True:
    reading = adc.read_u16() * conversion_factor # read temperature sensor
    temperature = 27 - (reading - 0.706)/0.001721 #convert voltage value to degrees celsius
    i2c.writeto(114, '\x7C') #enter settings mode
    i2c.writeto(114, '\x2D') #clear display
    out_string = "   DIYODE MAG     TEMP: " + str(round(temperature, 1)) + "\xDFC" #construct string to print
    i2c.writeto(114, out_string) #print text to display
    led_onboard.toggle()
    utime.sleep(1) 