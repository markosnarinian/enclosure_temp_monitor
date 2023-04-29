from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from dht import DHT11

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

lcd.clear()
lcd.putstr("DHT11 TEMP &\nHUMIDITY MONITOR")
sleep(5)
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("RH:--% TEMP:--")
lcd.move_to(0, 1)
lcd.putstr("RH:--% TEMP:--")


sensor1 = DHT11(Pin(14))
sensor2 = DHT11(Pin(15))

while True:
    try:
        sensor1.measure()
    except:
        rh1 = "--"
        temp1 = "--"
    else:
        rh1 = sensor1.humidity()
        temp1 = sensor1.temperature()

        if rh1 > 99: rh1 = 99
        if temp1 > 99: temp1 = 99

        rh1 = str(rh1)
        temp1 = str(temp1)
        
        if len(rh1) == 1: rh1 = " " + rh1
        if len(temp1) == 1: temp1 = " " + temp1

    try:
        sensor2.measure()
    except:
        rh2 = "--"
        temp2 = "--"
    else:
        rh2 = sensor2.humidity()
        temp2 = sensor2.temperature()

        if rh2 > 99: rh2 = 99
        if temp2 > 99: temp2 = 99

        rh2 = str(rh2)
        temp2 = str(temp2)
        
        if len(rh2) == 1: rh2 = " " + rh2
        if len(temp2) == 1: temp2 = " " + temp2

    print(f"\nRH1: {rh1}, TEMP1: {temp1}\nRH2: {rh2}, TEMP2: {temp2}")

    lcd.move_to(3,0)
    lcd.putstr(str(rh1))
    lcd.move_to(12,0)
    lcd.putstr(str(temp1))

    lcd.move_to(3,1)
    lcd.putstr(str(rh2))
    lcd.move_to(12,1)
    lcd.putstr(str(temp2))

    sleep(1)
