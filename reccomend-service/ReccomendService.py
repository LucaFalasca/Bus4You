import json
import xmlrpc.server


def get_future_confirmed_routes_by_db():

    with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
        routes = json.loads(proxy.get_future_confirmed_routes())

    final_route = {}

    for route in routes:
        index = get_index(final_route.get(route[0], []), route[1])
        if index is None:
            final_route.setdefault(route[0], []).append({
                "step": route[1], 
                "name": route[2],
                "position": [float(route[3]), float(route[4])], 
                "timestamp": route[5],
                "climb_up": route[6],
                "climb_down": route[7]
            })
        else:
            final_route[route[0]][index]["climb_up"] += route[6]
            final_route[route[0]][index]["climb_down"] += route[7]
    return final_route

def get_index(lista, valore):
    indice = None
    for i, d in enumerate(lista):
        if d["step"] == valore:
            indice = i
            break
    return indice

def get_future_confirmed_routes():
    routes = []
    max = 8
    routes_raw = get_future_confirmed_routes_by_db()
    for route_id, itinerari in routes_raw.items():
        print(route_id)
        steps = [0] * len(itinerari)
        print(steps)
        for it in itinerari:
            print(it)
            steps[it['step'] - 1] = it

        segments = []
        seat_available = 0
        for i in range(len(steps) - 1):
            if i == 0:
                seat_available = max - steps[0]["climb_up"]
            else:
                seat_available = seat_available - steps[i]["climb_up"] + steps[i]["climb_down"]
            segments.append({
                "start": steps[i]["position"],
                "end": steps[i+1]["position"],
                "seat_available" : seat_available
            })
        r = {
            "route" : route_id,
            "steps" : steps,
            "segments" : segments
        }
        routes.append(r)
    print(routes)
    return json.dumps(routes)

    

if __name__ == "__main__":
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")
    server.register_function(get_future_confirmed_routes, "get_future_confirmed_routes")
    server.serve_forever()
    