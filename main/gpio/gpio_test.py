import Jetson.GPIO as GPIO
from paho.mqtt import client as mqtt_client
import time
import random
import json
broker = 'r201_nx.local'
port = 1883
# topic = "/bot/chassis"
client_id = f'gpio-{random.randint(0, 1000)}'
def connect_mqtt():#連接伺服器
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def go(client: mqtt_client,led1,led2):

    print("go")
    GPIO.output(led1, GPIO.HIGH)
    GPIO.output(led2, GPIO.LOW)
    # client.publish(topic="/bot/log", payload=json.dumps({"msg": "log.play"}), qos=0)
      
            
    # client.subscribe(topic)
    # client.on_message = on_message

def run():
    client = connect_mqtt()
    GPIO.setmode(GPIO.BOARD)
    mode = GPIO.getmode()
    print(mode)
    channel=32
    a1=29
    a2=31
    led1=15
    led2=33
    GPIO.setup(a1, GPIO.IN)
    GPIO.setup(led1, GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(led2, GPIO.OUT,initial=GPIO.HIGH)

    GPIO.setup(channel, GPIO.IN)
    GPIO.setup(a2, GPIO.IN)
    # client.loop_start()
    while 1:
        print(GPIO.input(channel),GPIO.input(a1),GPIO.input(a2))
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.LOW)
        if GPIO.input(channel):
            go(client,led1,led2)
            time.sleep(5)

        client.loop_start()    
    # subscribe(client)
    
    
    # client.loop_forever()
if __name__ == '__main__':
    # i2c.ress()
    run()  


