import random
import time
import xmlrpc.client
import datetime
from collections import OrderedDict
from circuitbreaker import circuit

import requests
from flask import Flask, json, request, Response, jsonify

api = Flask(__name__)


@circuit
@api.route('/api/login', methods=['GET'])
def login():
    mail = request.args.get('usr')
    password = request.args.get('pwd')
    with xmlrpc.client.ServerProxy("http://login-service:8000/") as proxy:
        result = proxy.rpc_login(mail, password)
        return json.dumps(result)


@circuit
@api.route('/api/sign-up', methods=['GET'])
def signUp():
    name = request.args.get('name')
    surname = request.args.get('surname')
    mail = request.args.get('mail')
    password = request.args.get('pwd')
    birthdate = request.args.get('birthdate')
    username = request.args.get('usr')
    with xmlrpc.client.ServerProxy("http://login-service:8000/") as proxy:
        result = proxy.rpc_sign_up(name, surname, mail, password, birthdate, username)
        return json.dumps(result)


@circuit
@api.route('/api/route-from-map', methods=['GET'])
def route_from_map():
    try:
        user = request.args.get('user')
        starting_point = request.args.get('starting_point')
        start_lat = request.args.get('start_lat')
        start_lng = request.args.get('start_lng')
        ending_point = request.args.get('ending_point')
        end_lat = request.args.get('end_lat')
        end_lng = request.args.get('end_lng')
        date = request.args.get('date')
        start_or_finish = request.args.get('start-finish')
        print("SOF" + start_or_finish)
        time = request.args.get('time')
        print(user, starting_point, ending_point, date, start_or_finish, time, start_lat, start_lng, end_lat, end_lng)
        with xmlrpc.client.ServerProxy("http://booking_service:8000/") as proxy:
            result = proxy.insert_booking(user, starting_point, start_lat, start_lng, ending_point, end_lat, end_lng,
                                          date,
                                          start_or_finish, time)
            print(result)
            return Response(json.dumps({"status": "ok", "it_req_id": result}), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


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


@circuit
@api.route('/api/load_user_routes', methods=['GET'])
def load_user_routes():
    mail = request.args.get('user')
    ret = []
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        user_routes = json.loads(proxy.get_user_routes(mail))
    for route in user_routes:
        ret.append({"it_cost": route[0], "it_prop_start": route[1], "it_prop_end": route[2], "it_status": route[3],
                    "route_past": route[4], "route_status": route[5], "route_expire": route[6], "start_stop": route[7],
                    "end_stop": route[8], "it_id": route[9]})

    return json.dumps(ret)


@circuit
@api.route('/api/get_bus_stops', methods=['GET'])
def get_bus_stops():
    ret = []
    try:
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            bus_stops = json.loads(proxy.get_stops())
        for elem in bus_stops:
            stop = {"name": elem[0], "lat": elem[1], "lang": elem[2]}
            ret.append(stop)
        if not ret:
            return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')
        else:
            return Response(json.dumps({"status": "ok", "stop_list": ret}), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_bus_stops_rect', methods=['GET'])
def get_bus_stops_rect():
    try:
        ret = []
        x = request.args.get('x')
        y = request.args.get('y')
        height = request.args.get('height')
        width = request.args.get('width')
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            bus_stops = json.loads(proxy.get_stops_rect(x, y, height, width))
        for elem in bus_stops:
            stop = {"name": elem[0], "lat": elem[1], "lang": elem[2]}
            ret.append(stop)
        return Response(json.dumps({"status": "ok", "data": ret}), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_path', methods=['POST'])
def get_path():
    data = request.get_json()
    print(data)
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.get_stops_from_it(data)
        print(ret)
        stops = json.loads(ret)
    url = 'http://ors-app:8080/ors/v2/directions/driving-car/geojson'
    body = {}
    print(stops)
    true_stops = [[float(s[2]), float(s[1])] for s in stops]
    body['coordinates'] = true_stops
    print(body)
    result = requests.post(url, json=body).json()
    print(result)
    coords = result["features"][0]["geometry"]["coordinates"]
    print(coords)
    coords_reversed = [coord[::-1] for coord in coords]
    final_ret = {"coordinates": coords_reversed, "stops": true_stops}
    return json.dumps(final_ret)


@circuit
@api.route('/api/get_path_from_stops', methods=['POST'])
def get_path_from_stops():
    stops = request.get_json()
    print(stops)
    url = 'http://ors-app:8080/ors/v2/directions/driving-car/geojson'
    body = {}
    print(stops)
    true_stops = [[float(s[1]), float(s[0])] for s in stops]
    body['coordinates'] = true_stops
    print(body)
    result = requests.post(url, json=body).json()
    print(result)
    coords = result["features"][0]["geometry"]["coordinates"]
    print(coords)
    coords_reversed = [coord[::-1] for coord in coords]
    final_ret = {"coordinates": coords_reversed, "stops": true_stops}
    return json.dumps(final_ret)


@circuit
@api.route('/api/confirm_it', methods=['GET'])
def confirm_it():
    it_id = request.args.get('it_id')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.confirm_it(it_id)
        # print(ret)
        return json.dumps(ret)


@circuit
@api.route('/api/reject_it', methods=['GET'])
def reject_it():
    it_id = request.args.get('it_id')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.reject_it(it_id)
        print(ret)
        return json.dumps(ret)


@circuit
@api.route('/api/get_retry_info', methods=['GET'])
def get_retry_info():
    it_id = request.args.get('it_id')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.get_retry_info(it_id)
        # print(ret)
        return json.dumps(ret)


@circuit
@api.route('/api/get_user_balance', methods=['GET'])
def get_user_balance():
    mail = request.args.get('user')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.get_user_balance(mail)
        # print("Gateway balance",ret)
        return json.dumps(ret)


@circuit
@api.route('/api/get_future_confirmed_routes', methods=['GET'])
def get_future_confirmed_routes():
    with xmlrpc.client.ServerProxy("http://reccomend-service:8000/") as proxy:
        ret = proxy.get_future_confirmed_routes()
        print(ret)
        return json.dumps(ret)


@circuit
@api.route('/api/get_total_km', methods=['GET'])
def get_total_km():
    route_id = request.args.get('route_id')
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = proxy.get_total_km(route_id)
        print(ret)
        return json.dumps(ret)


@circuit
@api.route('/api/get_km_price_from_subroute', methods=['POST'])
def get_km_price_from_subroute():
    try:
        print("REQUEST" + str(request))
        request_value = request.get_json()
        stops = request_value["bus_stops"]
        print(stops)
        true_stops = [[float(s[1]), float(s[0])] for s in stops]
        body = {}
        body['coordinates'] = true_stops
        url = 'http://ors-app:8080/ors/v2/directions/driving-car/geojson'
        print(stops)
        true_stops = [[float(s[1]), float(s[0])] for s in stops]
        body['coordinates'] = true_stops
        print(body)
        result = requests.post(url, json=body).json()
        print(result)
        distance = result["features"][0]["properties"]["summary"]["distance"]
        print(distance)

        route_id = request_value['route']
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            ret = json.loads(proxy.get_total_km(route_id))
            print(ret)
        total_km = ret[0][0]
        total_price = ret[0][1]

        print("DISTANCE" + str(distance))
        print("TOTAL KM" + str(total_km))
        print("TOTAL PRICE" + str(total_price))

        weight = distance / (float(total_km) * 1000 + distance)
        price = float(total_price) * weight + 0.3

        final_ret = {"price": round(price, 2),
                     "distance": distance}
        print(final_ret)
        return Response(json.dumps({"status": "ok", "price": final_ret["price"], "distance": final_ret["distance"]}),
                        status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/join_recommended_route', methods=['GET', 'POST'])
def join_recommended_route():
    try:
        route_id = request.args.get('route_id')
        start_lat = request.args.get('start_lat')
        start_lng = request.args.get('start_lng')
        end_lat = request.args.get('end_lat')
        end_lng = request.args.get('end_lng')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        price = request.args.get('price')
        distance = request.args.get('distance')
        mail = request.args.get('user')
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            ret = proxy.join_recommended_route(route_id, start_lat, start_lng, end_lat, end_lng, start_date, end_date,
                                               price, distance, mail)
            print(ret)
            return Response(json.dumps(ret), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_token', methods=['GET', 'POST'])
def get_token():
    try:
        with xmlrpc.client.ServerProxy("http://login-service:8000/") as proxy:
            ret = proxy.rpc_get_token()
        if ret['status'] == 'ok':
            return Response(json.dumps(ret), status=200, mimetype='application/json')
        else:
            return Response(json.dumps(ret), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


'''@api.route('/api/get_bus_stops', methods=['GET', 'POST'])
def get_bus_stops_api():
    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        ret = json.loads(proxy.get_stops())
    if not ret:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')
    else:
        return Response(json.dumps({"status": "ok", "stop_list": ret}), status=200, mimetype='application/json')'''


@circuit
@api.route('/api/get_itinerari_richiesti', methods=['GET', 'POST'])
def get_itinerari_richiesti():
    try:
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            ret = json.loads(proxy.get_itinerari_richiesti())
        if ret['status'] == 'ok':
            return Response(json.dumps(ret, sort_keys=False), status=200, mimetype='application/json')
        else:
            return Response(json.dumps(ret, sort_keys=False), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_itinerari_proposti', methods=['GET', 'POST'])
def get_itinerari_proposti():
    try:
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            ret = json.loads(proxy.get_itinerari_proposti())
        if ret['status'] == 'ok':
            return Response(json.dumps(ret, sort_keys=False), status=200, mimetype='application/json')
        else:
            return Response(json.dumps(ret, sort_keys=False), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_routes', methods=['GET', 'POST'])
def get_routes():
    try:
        with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
            ret = json.loads(proxy.get_routes())
        if ret['status'] == 'ok':
            return Response(json.dumps(ret, sort_keys=False), status=200, mimetype='application/json')
        else:
            return Response(json.dumps(ret, sort_keys=False), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/make-route-raw', methods=['POST'])
def make_route_raw():
    try:
        request_value = request.get_json()
        print(request_value)
        dist_matrix = request_value["dist_matrix"]
        prec_hash = request_value["prec_hash"]
        node_limit = request_value["node_limit"]
        user_routes = request_value["user_routes"]
        date_string = user_routes[0]["date"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        print(dist_matrix)
        print(prec_hash)
        print(node_limit)
        print(user_routes)

        with xmlrpc.client.ServerProxy("http://make-route-service:8000/", allow_none=True) as proxy:
            result = proxy.calculate_route(dist_matrix, prec_hash, node_limit, user_routes)
            result_json = {}
            route = result[0][0]
            steps = []
            for step in route:
                step_json = {}
                step_json["id"] = step[0]
                time = round(float(step[1]), 0)
                if time > 0 and time < 1440:
                    step_json["date"] = str(date)[0:10]
                    step_json["time"] = str(datetime.timedelta(minutes=(time)))
                elif time < 0:
                    step_json["date"] = str(date + datetime.timedelta(days=-1))[0:10]
                    step_json["time"] = str(datetime.timedelta(minutes=1440 + time))
                elif time > 1440:
                    step_json["date"] = str(date + datetime.timedelta(days=1))[0:10]
                    step_json["time"] = str(datetime.timedelta(minutes=time - 1440))
                steps.append(step_json)
            result_json["steps"] = steps
            result_json["travel_time"] = str(datetime.timedelta(minutes=round(float(result[0][1]), 0)))
            result_json["n_tardy"] = result[0][2]
            result_json["mean_unacceptable_deviance"] = str(datetime.timedelta(minutes=round(result[0][3])))
            result_json["users_travel_time"] = result[1]
            result_json["user_routes"] = user_routes
            return Response(json.dumps(result_json), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/make-route', methods=['POST'])
def make_route():
    try:
        request_value = request.get_json()
        print(request_value)
        points_location = request_value["points_location"]
        input_ors = [q[::-1] for q in list(points_location.values())]
        with xmlrpc.client.ServerProxy("http://ors-dao:8000/", allow_none=True) as proxy:
            dist_matrix = proxy.get_matrix(input_ors)
        prec_hash = request_value["prec_hash"]
        node_limit = request_value["node_limit"]
        user_routes = request_value["user_routes"]
        date_string = user_routes[0]["date"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        print(dist_matrix)
        print(prec_hash)
        print(node_limit)
        print(user_routes)

        with xmlrpc.client.ServerProxy("http://make-route-service:8000/", allow_none=True) as proxy:
            result = proxy.calculate_route(dist_matrix, prec_hash, node_limit, user_routes)
            result_json = {}
            route = result[0][0]
            steps = []
            for step in route:
                step_json = {}
                step_json["id"] = step[0]
                time = round(float(step[1]), 0)
                if time > 0 and time < 1440:
                    step_json["date"] = str(date)[0:10]
                    step_json["time"] = str(datetime.timedelta(minutes=(time)))
                elif time < 0:
                    step_json["date"] = str(date + datetime.timedelta(days=-1))[0:10]
                    step_json["time"] = str(datetime.timedelta(minutes=1440 + time))
                elif time > 1440:
                    step_json["date"] = str(date + datetime.timedelta(days=1))[0:10]
                    step_json["time"] = str(datetime.timedelta(minutes=time - 1440))
                step_json["location"] = request_value["points_location"][str(step[0])][::-1]
                steps.append(step_json)
            result_json["steps"] = steps
            result_json["travel_time"] = str(datetime.timedelta(minutes=round(float(result[0][1]), 0)))
            result_json["n_tardy"] = result[0][2]
            result_json["mean_unacceptable_deviance"] = str(datetime.timedelta(minutes=round(result[0][3])))
            result_json["users_travel_time"] = result[1]
            result_json["user_routes"] = user_routes
            return Response(json.dumps(result_json), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_recommended_routes', methods=['POST', 'GET'])
def get_recommended_routes():
    try:
        with xmlrpc.client.ServerProxy("http://reccomend-service:8000/", allow_none=True) as proxy:
            result = proxy.get_future_confirmed_routes()
        res = {"status": "ok", "recommended-routes-list":json.loads(result)}
        return Response(json.dumps(res, sort_keys=False), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_random_cluster_from_it_id', methods=['GET'])
def get_random_cluster_from_it_id():
    try:
        it_id = request.args.get('it_id')

        with xmlrpc.client.ServerProxy("http://node-selector-service:8000/") as proxy:
            ret = proxy.get_random_cluster_from_it_id(it_id)
            return Response(json.dumps(ret), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_all_clusters', methods=['GET'])
def get_all_clusters():
    try:

        with xmlrpc.client.ServerProxy("http://node-selector-service:8000/") as proxy:
            ret = proxy.get_all_clusters()
            return Response(json.dumps(ret), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')


@circuit
@api.route('/api/get_random_cluster', methods=['GET'])
def get_random_cluster():
    try:

        with xmlrpc.client.ServerProxy("http://node-selector-service:8000/") as proxy:
            ret = proxy.get_random_cluster()
            return Response(json.dumps(ret), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')

@api.route('/api/get_bus_status', methods=['GET'])
def get_bus_status():
    try:
        smart_gc_url = "https://webapp.smartcity.uniupo.click/api/riempimenti/" + str(request.args.get('bus_id'))
        status = requests.get(smart_gc_url).json()
        return Response(json.dumps(status), status=200, mimetype='application/json')
    except:
        return Response(json.dumps({"status": "error"}), status=400, mimetype='application/json')

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=50052)
