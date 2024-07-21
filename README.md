# mqtt-to-kafka

```shell
# 构建镜像
docker build -t <image-tag> .

# 构建其他cpu架构的镜像
docker build \
-t <image-tag> \
--platform=linux/arm64 \
-o type=docker .


# 运行
docker run \
--name mqtt-to-kafka \
-e MQTT_CLIENT_ID="deepexi-test" \
-e MQTT_BROKER_HOST="mqtt.eclipseprojects.io" \
-e MQTT_BROKER_PORT=1883 \
-e MQTT_USER_NAME="admin" \
-e MQTT_PASSWORD="admin" \
-e BOOTSTRAP_SERVER="172.20.3.26:9094" \
-e TOPIC_MAPPING="$SYS/#:mqtt" \
<image-tag>
```

3. 配置说明
- MQTT_CLIENT_ID：客户端id，可不配置
- MQTT_BROKER_HOST：mqtt broker的IP地址
- MQTT_BROKER_PORT：mqtt broker的端口，默认1883
- MQTT_USER_NAME/MQTT_PASSWORD：连接mqtt broker的用户名/密码，若不需要则不配置
- BOOTSTRAP_SERVER：kafka的连接地址
- TOPIC_MAPPING：mqtt topic和kafka topic的映射关系，将一个mqtt topic或一组mqtt topic（通配符的方式）的消息转发到kafka的topic，支持多组映射，格式：mqtt_topic1:kafka_topic1,mqtt_topic2:kafka_topic2...
4. 发送到kafka的消息格式
   
发送到kafka的消息是json格式：

```json
{
   "topic": "/sys/aaaa/bbbb/thing/event/property/post", // mqtt的topic全名
   "payload": "{...}", // 接受到的消息，可能也是一个json对象
   "report_time": "2024-07-21 12:01:44.727" // 数据接收时间戳（毫秒）
}
```   
