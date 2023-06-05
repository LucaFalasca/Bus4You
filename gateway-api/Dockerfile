# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN ["python3", "-m", "grpc_tools.protoc", "--proto_path=./gatewayApi", "--python_out=./gatewayApi", "--pyi_out=./gatewayApi", "--grpc_python_out=./gatewayApi", "./gatewayApi/protos/login_service_cs.proto"]
RUN chmod 777 ./gatewayApi/protos/login_service_cs_pb2.py
RUN chmod 777 ./gatewayApi/protos/login_service_cs_pb2.pyi
RUN chmod 777 ./gatewayApi/protos/login_service_cs_pb2_grpc.py

CMD ["python3", "./gatewayApi/GatewayApi.py"]