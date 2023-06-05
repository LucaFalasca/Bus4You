# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN ["python3", "-m", "grpc_tools.protoc", "--proto_path=./loginService", "--python_out=./loginService", "--pyi_out=./loginService", "--grpc_python_out=./loginService", "./loginService/protos/login_service_ss.proto"]
RUN chmod 777 ./loginService/protos/login_service_ss_pb2.py
RUN chmod 777 ./loginService/protos/login_service_ss_pb2.pyi
RUN chmod 777 ./loginService/protos/login_service_ss_pb2_grpc.py

CMD ["python3", "./loginService/LoginService.py"]