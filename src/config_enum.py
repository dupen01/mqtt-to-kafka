from enum import Enum


class ConfigEnum(Enum):
    mqtt_broker_host = "MQTT_BROKER_HOST"
    mqtt_broker_port = "MQTT_BROKER_PORT"
    mqtt_client_id = "MQTT_CLIENT_ID"
    mqtt_user_name = "MQTT_USER_NAME"
    mqtt_password = "MQTT_PASSWORD"
    bootstrap_server = "BOOTSTRAP_SERVER"
    topic_mapping = "TOPIC_MAPPING"
