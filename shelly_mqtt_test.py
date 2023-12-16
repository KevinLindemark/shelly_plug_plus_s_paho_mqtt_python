# https://plainenglish.io/blog/mqtt-beginners-guide-in-python-38590c8328ae
# https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Mqtt/

import time
import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid):
    print("sent a message")


mqttClient = mqtt.Client("pi5")
mqttClient.on_publish = on_publish
mqttClient.connect('192.168.1.153', 1883)
# start a new thread
mqttClient.loop_start()

mqttClient.subscribe('shellies/shellyplusplugs-d4d4dae8639c/')

# https://shelly-api-docs.shelly.cloud/gen2/General/RPCChannels#MQTT
# publish this to turn switch on or change true to false to turn off
# {"id":123, "src":"user_1", "method":"Switch.Set", "params":{"id":0,"on":true}}

# Why use msg.encode('utf-8') here
# MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
# Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
while True:
    msg_user = input("MQTT message")
    info = mqttClient.publish(
        topic='shellyplusplugs-d4d4dae8639c/rpc',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)
