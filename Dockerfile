# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
FROM registry.cn-chengdu.aliyuncs.com/mirror_d/uv:python3.13-bookworm-slim

COPY src /app/src
COPY pyproject.toml uv.lock /app/

WORKDIR /app 
RUN uv sync --default-index https://mirrors.aliyun.com/pypi/simple/ --frozen

CMD ["uv", "run", "src/mqtt_to_kafka.py"]
