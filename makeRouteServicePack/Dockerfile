# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN ["python3", "-m", "grpc_tools.protoc", "--proto_path=./makeRouteService", "--python_out=./makeRouteService", "--pyi_out=./makeRouteService", "--grpc_python_out=./makeRouteService", "./loginService/protos/make_route_service_ss.proto"]

CMD ["python3", "./makeRouteService/2-opt.py"]
