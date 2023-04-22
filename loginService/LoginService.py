from dao.user_db import UserDbDao as usrDb
import grpc
import protos.login_service_pb2_grpc
import protos.login_service_pb2
from concurrent import futures

from dao.user_db.UserDbDao import UserDbDao


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protos.login_service_pb2_grpc.add_LoginServicer_to_server(LoginService(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()


class LoginService(protos.login_service_pb2_grpc.LoginServicer):
    def RpcLogin(self, request, context):
        usr_db = UserDbDao()
        conn = usr_db.connect()
        log_ret = usr_db.login_query(conn, request.username, request.password)
        conn.close()
        if log_ret == 0:
            print("Login successful")
            return protos.login_service_pb2.LoginResponse(message="Login successful", token="TokenDiProva")
        elif log_ret == 1:
            print("Login failed")
            return protos.login_service_pb2.LoginResponse(message="Login failed")
        else:
            print("Connection with db failed")
            return protos.login_service_pb2.LoginResponse(message="Connection with db failed")


if __name__ == "__main__":
    serve()
