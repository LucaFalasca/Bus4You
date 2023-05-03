import hashlib
from concurrent import futures

import grpc

import protos.login_service_ss_pb2
import protos.login_service_ss_pb2_grpc
from dao.user_db.UserDbDao import UserDbDao


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protos.login_service_ss_pb2_grpc.add_LoginServicer_to_server(LoginService(), server)
    # server.add_insecure_port('localhost:50051')
    server.add_insecure_port('[::]:50051')  # For docker
    server.start()
    server.wait_for_termination()


class LoginService(protos.login_service_ss_pb2_grpc.LoginServicer):
    def RpcLogin(self, request, context):
        usr_db = UserDbDao()
        conn = usr_db.connect()
        log_ret = usr_db.login_query(conn, request.username, request.password)
        conn.close()
        if log_ret == 0:
            print("Login successful")
            token = hashlib.md5((request.username+request.password).encode('utf-8')).hexdigest()
            return protos.login_service_ss_pb2.LoginResponse(message="Login successful", token=token)
        elif log_ret == 1:
            print("Login failed")
            return protos.login_service_ss_pb2.LoginResponse(message="Login failed")
        else:
            print("Connection with db failed")
            return protos.login_service_ss_pb2.LoginResponse(message="Connection with db failed")


if __name__ == "__main__":
    serve()
