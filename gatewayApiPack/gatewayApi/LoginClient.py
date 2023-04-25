import protos.login_service_cs_pb2
import grpc


if __name__ == "__main__":
    channel = grpc.insecure_channel('localhost:50051')
    stub = protos.login_service_cs_pb2_grpc.LoginStub(channel)
    login_request = protos.login_service_cs_pb2.LoginCredentials(username="prova", password="1234")
    response = stub.RpcLogin(login_request)
    print("LoginService client received: " + response.message + " Token: " + response.token)