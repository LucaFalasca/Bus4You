import grpc
from flask import Flask, json, request

import protos.login_service_cs_pb2
import protos.login_service_cs_pb2_grpc

api = Flask(__name__)


@api.route('/login', methods=['GET'])
def login():
    res = {}
    username=request.args.get('usr')
    password=request.args.get('pwd')
    channel = grpc.insecure_channel(
        'login-service:50051')  # Insert the name of the service as IP if using docker network
    stub = protos.login_service_cs_pb2_grpc.LoginStub(channel)
    login_request = protos.login_service_cs_pb2.LoginCredentials(username=username, password=password)
    response = stub.RpcLogin(login_request)
    res['message'] = response.message
    res['token'] = response.token
    print("LoginService client received: " + response.message + " Token: " + response.token)
    return json.dumps(res)


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=50052)
