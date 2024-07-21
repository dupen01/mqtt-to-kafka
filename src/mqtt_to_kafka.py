import json
import os
import datetime
import re
import logging
import socket

from config_enum import ConfigEnum

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from paho.mqtt import client as mqtt


# set logger
logger = logging.getLogger('test-name')
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def on_connect(client: mqtt.Client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logger.info(f"Connected to MQTT Broker: {broker}:{port}")
    else:
        logger.error(f"Failed to connect, return code {reason_code}")
    for x in topic_mapping.split(','):
        client.subscribe(x.split(':')[0])


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    # 定义发送到kafka的消息格式
    kafka_msg = {}
    kafka_msg.setdefault('topic', msg.topic)
    kafka_msg.setdefault('payload', msg.payload.decode())
    kafka_msg.setdefault('report_time', str(datetime.datetime.now())[:23])
    # 封装为json
    kafka_value = json.dumps(kafka_msg).encode('utf-8')

    # send to kafka
    try:
        producer = KafkaProducer(bootstrap_servers=bootstrap_server)
        for x in topic_mapping.split(','):
            mq_topic = x.split(':')[0]
            kk_topic = x.split(':')[1]
            mq_topic2 = mq_topic.replace('$', "\\$")
            is_match = re.match(re.sub(r'[+#]', '.*', mq_topic2), msg.topic)
            if msg.topic == mq_topic or is_match:
                producer.send(kk_topic, key=msg.topic.encode(), value=kafka_value)
                logger.info(f'(kafka) {mq_topic} -> {kk_topic}: {kafka_msg}')
    except NoBrokersAvailable:
        # logger.error(f"kafka broker not available: {bootstrap_server}")
        # 若kafka broker不可用，仅打印mqtt的消息日志
        logger.info(f"(mqtt) {msg.topic}: {msg.payload.decode()}")


def run():
    logger.info(f"mqtt_broker: {broker}:{port}")
    logger.info(f"mqtt_client_id: {client_id}")
    logger.info(f"bootstrap_server: {bootstrap_server}")
    logger.info(f"topic_mapping: {topic_mapping}")
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    mqttc.username_pw_set(username=user_name, password=password)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(broker, port, 60)
    mqttc.loop_forever()


broker = os.environ.get(ConfigEnum.mqtt_broker_host.value) \
    if os.environ.get(ConfigEnum.mqtt_broker_host.value) else 'mqtt.eclipseprojects.io'
port = int(os.environ.get(ConfigEnum.mqtt_broker_port.value)) \
    if os.environ.get(ConfigEnum.mqtt_broker_port.value) else 1883
client_id = os.environ.get(ConfigEnum.mqtt_client_id.value) \
    if os.environ.get(ConfigEnum.mqtt_client_id.value) else f"{socket.gethostname()}-{os.getuid()}"

user_name = os.environ.get(ConfigEnum.mqtt_user_name.value)
password = os.environ.get(ConfigEnum.mqtt_password.value)

bootstrap_server = os.environ.get(ConfigEnum.bootstrap_server.value) \
    if os.environ.get(ConfigEnum.bootstrap_server.value) else '127.0.0.1:9092'

topic_mapping = os.environ.get(ConfigEnum.topic_mapping.value) \
    if os.environ.get(ConfigEnum.topic_mapping.value) else '$SYS/#:mqtt'

# TODO: 做测试用，正式环境需删除
# broker = 'mqtt.eclipseprojects.io'
# topic_mapping = '$SYS/#:mqtt'
# bootstrap_server = "172.20.3.26:9094"


run()
