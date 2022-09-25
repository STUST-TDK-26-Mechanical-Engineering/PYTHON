from paho.mqtt import client as mqtt_client
import random
import json
from PitchingSerial import main
broker = 'r201_nx.local'
port = 1883
topic = "/bot/pitching"
client_id = f'pitching-{random.randint(0, 1000)}'
pitching=main()
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

def subscribe(client: mqtt_client):#訂閱
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        m_in=json.loads(msg.payload.decode()) #decode json data
        print(m_in["msg"])
        
        if m_in["msg"]=="pitching.play":
            if m_in["mode"]=="0x01":
                pitching.origin()
            elif m_in["mode"]=="0x02":
                pitching.run_90_degrees()    


                   
            
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
if __name__ == '__main__':
    run()  


