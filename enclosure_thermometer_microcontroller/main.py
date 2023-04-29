from machine import I2C, Pin
from time import sleep, sleep_ms, time
from pico_i2c_lcd import I2cLcd
import urequests
from json import loads
import onewire
import ds18x20
import network
import socket
import _thread

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

try:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("SENSITIVE DATA", "SENSITIVE DATA")
    while wlan.isconnected() == False:
        pass
except:
    #print("Failed to connect to WLAN network")
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Unable to")
    lcd.move_to(0,1)
    lcd.putstr("connect to WLAN")
else:
    #print(wlan.ifconfig())
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Connected")
    lcd.move_to(0,1)
    lcd.putstr(wlan.ifconfig()[0])
    
sleep(2)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("--- -- --- --:--")
lcd.move_to(0, 1)
lcd.putstr("TEMP: --.-")

ds_pin = machine.Pin(27)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()

line1 = "--- -- --- --:--"

time_at_sync = time() - 10
while True:
    try:
        ds_sensor.convert_temp()
    except:
        temp = "--.-"
    else:
        temp = '%.1f'%(ds_sensor.read_temp(roms[0]))
        #print(temp)
        
    lcd.move_to(0,0)
    lcd.putstr(line1)

    lcd.move_to(6,1)
    lcd.putstr(temp)
    
    #print((time_at_sync + 10)-time())
    if time() >= time_at_sync + 10:
        try:
            r=urequests.get(f"http://192.168.1.12:50110/exchange?temp={temp}", timeout=2)
            line1 = r.text
            print(line1)
        except:
            line1 = "--- -- --- --:--"
            
        time_at_sync = time()

    sleep(0.5)
