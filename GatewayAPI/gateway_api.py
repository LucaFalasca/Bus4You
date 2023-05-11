import xmlrpc.client

import random
import time
from flask import Flask, render_template, request, json

app = Flask(__name__)

@app.route('/RequestRoute', methods=['GET'])
def request_route():
    starting_point = request.args.get('starting_point')
    ending_point = request.args.get('ending_point')

    dist_matrix = generate_dist_matrix(20, 10)
    pred_hash = {"0":4, "1":3, "7":8, "3":6, "4":11, "5":14, "0":9, "6":9, "8":9, "11":15, "11":14, "18":11, "13":12, "14":17, "15":19, "16":18, "17":19, "18":19}
    route = [0, 2, 1, 3, 6, 5, 4, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10]
    with xmlrpc.client.ServerProxy("http://server:8000/") as proxy:
        result = proxy.two_opt_multistart(route, dist_matrix, pred_hash, 10)
        return render_template("response_route.html", 
                               route=result[0], 
                               distance=result[1], 
                               starting_point=starting_point, 
                               ending_point=ending_point)

@app.route('/')
def index():
    return render_template("request_route.html")

@app.route('/api/route-from-map', methods=['GET'])
def route_from_map():
    if (len(request.args) == 0):
        return render_template("select_route_from_map.html")
    else:
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


