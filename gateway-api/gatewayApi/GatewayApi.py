import grpc
from flask import Flask, json, request
import xmlrpc.client

import random
import time

import protos.login_service_cs_pb2
import protos.login_service_cs_pb2_grpc

api = Flask(__name__)


@api.route('/api/login', methods=['GET'])
def login():
    res = {}
    username = request.args.get('usr')
    password = request.args.get('pwd')
    channel = grpc.insecure_channel(
        'login-service:50051')  # Insert the name of the service as IP if using docker network
    stub = protos.login_service_cs_pb2_grpc.LoginStub(channel)
    login_request = protos.login_service_cs_pb2.LoginCredentials(username=username, password=password)
    response = stub.RpcLogin(login_request)
    res['message'] = response.message
    res['token'] = response.token
    print("LoginService login client received: " + response.message + " Token: " + response.token)
    return json.dumps(res)


@api.route('/api/sign-up', methods=['GET'])
def signUp():
    res = {}
    name = request.args.get('name')
    surname = request.args.get('surname')
    mail = request.args.get('mail')
    password = request.args.get('pwd')
    birthdate = request.args.get('birthdate')
    username= request.args.get('usr')
    channel = grpc.insecure_channel(
        'login-service:50051')  # Insert the name of the service as IP if using docker network
    stub = protos.login_service_cs_pb2_grpc.LoginStub(channel)
    sign_up_request = protos.login_service_cs_pb2.SignUpCredentials(name=name, surname=surname, mail=mail, password=password, birthdate=birthdate, username=username)
    response = stub.RpcSignUp(sign_up_request)
    res['message'] = response.message
    res['token'] = response.token
    print("LoginService sign up client received: " + response.message + " Token: " + response.token)
    return json.dumps(res)

@api.route('/api/request-route', methods=['GET'])
def request_route():
    starting_point = request.args.get('starting_point')
    ending_point = request.args.get('ending_point')

    dist_matrix = generate_dist_matrix(20, 10)
    pred_hash = {"0": [1, 2], "1": [], "2": [4], "3": [4], "4": []}
    with xmlrpc.client.ServerProxy("http://make-root-service:8000/") as proxy:
        result = proxy.two_opt_multistart(dist_matrix, pred_hash)
        return json.dumps(result)

@api.route('/api/route-from-map', methods=['GET'])
def route_from_map():
    user = request.args.get('user')
    starting_point = request.args.get('starting_point')
    ending_point = request.args.get('ending_point')
    date = request.args.get('date')
    arrival_time = request.args.get('arrival_time')
    travel_time = request.args.get('travel_time')
    print(user, starting_point, ending_point, date, arrival_time, travel_time)
    with xmlrpc.client.ServerProxy("http://booking_service:8000/") as proxy:
        result = proxy.insert_booking(user, starting_point, ending_point, date, arrival_time, travel_time)
        return json.dumps(result)
        
        
def generate_dist_matrix(size, max_val):
    random.seed(time.time())
    dist_matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0)
            else:
                val = random.randint(1, max_val)
                row.append(val)
        dist_matrix.append(row)
    return dist_matrix


@api.route('/api/load_user_routes', methods=['GET'])
def load_user_routes():
    mail = request.args.get('mail')
    token = request.args.get('token')
    # TODO check token e retrieve delle route vere dal db
    user_routes = [{"startStop": "Alessandrino (MC)",
                   "endStop": "Sorbona",
                   "startHour": "10:00",
                   "endHour": "10:30",
                   "date": "24/05/2023",
                   "cost": "1.50€",
                   "stops": [
                       {"name": "Alessandrino (MC)", "pos": "xy"},
                       {"name": "Romanisti/Giaquinto", "pos": "xy"},
                       {"name": "Torre Maura", "pos": "xy"},
                       {"name": "Sorbona", "pos": "xy"}]},

                  {"startStop": "Sorbona",
                   "endStop": "Romanisti/Giaquinto",
                   "startHour": "17:00",
                   "endHour": "17:38",
                   "date": "24/05/2023",
                   "cost": "1.00€",
                   "stops": [
                       {"name": "Sorbona", "pos": "xy"},
                       {"name": "Torre Maura", "pos": "xy"},
                       {"name": "Romanisti/Torre Spaccata", "pos": "xy"},
                       {"name": "Casilina/Eriche", "pos": "xy"},
                       {"name": "Romanisti/Giaquinto", "pos": "xy"}]},

                  {"startStop": "Sium (MC[had])",
                   "endStop": "Chaddopia",
                   "startHour": "17:60",
                   "endHour": "18:00",
                   "date": "30/02/2345",
                   "cost": "0.99€",
                   "stops": [
                       {"name": "Sium (MC[had])", "pos": "xy"},
                       {"name": "Anor Londo", "pos": "xy"},
                       {"name": "Raftel", "pos": "xy"},
                       {"name": "Zanarkand", "pos": "xy"},
                       {"name": "Sparta", "pos": "xy"},
                       {"name": "Chaddopia", "pos": "xy"}]}]
    return json.dumps(user_routes)


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=50052)
