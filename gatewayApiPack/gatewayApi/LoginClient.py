import protos.login_service_cs_pb2
import protos.login_service_cs_pb2_grpc
import grpc
from flask import Flask, json

api = Flask(__name__)


@api.route('/login', methods=['GET'])
def get_companies():
    res={}
    channel = grpc.insecure_channel('localhost:50051')
    stub = protos.login_service_cs_pb2_grpc.LoginStub(channel)
    login_request = protos.login_service_cs_pb2.LoginCredentials(username="prova", password="1234")
    response = stub.RpcLogin(login_request)
    res['message'] = response.message
    res['token'] = response.token
    print("LoginService client received: " + response.message + " Token: " + response.token)
    return json.dumps(res)


if __name__ == '__main__':
    api.run()
