from machine import ADC, Pin, deepsleep
import utime
import time

lily_soil = ADC(Pin(32, Pin.IN)) # Soil moisture PIN reference
lily_soil.atten(ADC.ATTN_11DB)
jade_soil = ADC(Pin(33, Pin.IN)) # Soil moisture PIN reference
jade_soil.atten(ADC.ATTN_11DB)

#Calibraton values
lily_min_moisture=23000
lily_max_moisture=50000
#Calibraton values
jade_min_moisture=23000
jade_max_moisture=50000

readDelay = 57 # delay between readings

def connect_to_mqtt():
    global client_id, mqtt_server
    client = MQTTClient(client_id, mqtt_server)
    client.connect()

    return client


def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_to_mqtt()
except OSError as e:
  restart_and_reconnect()

while True:
    try:
        # read moisture value and convert to percentage into the calibration range
        lily_moisture = (lily_max_moisture-lily_soil.read_u16())*100/(lily_max_moisture-lily_min_moisture)
        lily_message = f'{lily_moisture:.2f}'
        # print values
        client.publish(lily_pub, lily_message.encode())

        # read moisture value and convert to percentage into the calibration range
        jade_moisture = (jade_max_moisture-jade_soil.read_u16())*100/(jade_max_moisture-jade_min_moisture)
        jade_message = f'{jade_moisture:.2f}'
        # print values
        client.publish(jade_pub, jade_message.encode())

        print(f'jade: {jade_moisture:.2f} ({jade_soil.read_u16()}), lily: {lily_moisture:.2f} ({lily_soil.read_u16()})')

        print("1 minutes deep sleep in 3s...")
        utime.sleep(3) # set a delay between readings
        print("Zzzzzzzzzzzz")
        deepsleep(readDelay * 1000)
    except OSError as e:
        restart_and_reconnect()
    

