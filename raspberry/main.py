from machine import Pin
import time
import network
import urequests as requests

from my_secrets import secrets


webserver_url = "http://192.168.2.12:1303/"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets['ssid'], secrets['pw'])

while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected")


led = Pin("LED", machine.Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led.off()


consecutive_open, consecutive_closed = 0, 0
door_open = button.value()

while True:
    button_val = button.value()
    
    if not button_val:
        consecutive_open = 0
        consecutive_closed += 1
    else:
        consecutive_open += 1
        consecutive_closed = 0
        
    if consecutive_open > 3 and not door_open:
        request = requests.get(webserver_url + 'opened')
        door_open = not door_open
    
    if consecutive_closed > 3 and door_open:
        request = requests.get(webserver_url + 'closed')
        door_open = not door_open
        
    time.sleep(0.1)

