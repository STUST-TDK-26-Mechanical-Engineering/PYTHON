import Jetson.GPIO as GPIO
from paho.mqtt import client as mqtt_client
import random
import json
broker = 'r201_nx.local'
port = 1883
# topic = "/bot/chassis"
client_id = f'chassis-{random.randint(0, 1000)}'
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
def go(client: mqtt_client):

    
    client.publish(topic="/bot/log", payload=json.dumps({"msg": "log.play"}), qos=0)
      
            
    # client.subscribe(topic)
    # client.on_message = on_message

def run():
    client = connect_mqtt()
    GPIO.setmode(GPIO.BOARD)
    mode = GPIO.getmode()
    print(mode)
    channel=40
    GPIO.setup(channel, GPIO.IN)
    # client.loop_start()
    while 1:
        print(GPIO.input(channel))
        if GPIO.input(channel):
            go(client)
        client.loop_start()    
    # subscribe(client)
    
    
    # client.loop_forever()
if __name__ == '__main__':
    # i2c.ress()
    run()  


