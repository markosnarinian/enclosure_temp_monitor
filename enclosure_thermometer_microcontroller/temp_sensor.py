import machine
import onewire
import ds18x20
import time

ds_pin = machine.Pin(27)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()

print("Found DS devices: " + str(roms))

ds_sensor.convert_temp()
time.sleep_ms(750)

for rom in roms:
    print(ds_sensor.read_temp(rom))
    time.sleep(1)