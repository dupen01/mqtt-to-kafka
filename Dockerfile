FROM python:3.9-slim-bullseye


COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY src/ /code/src/

CMD ["python3", "/code/src/mqtt_to_kafka.py"]
