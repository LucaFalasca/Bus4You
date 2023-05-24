from frontend.login.entity.stop import Stop
from frontend.login.entity.user_route import UserRoute


def parse_user_routes_json(response):
    user_routes = []
    for route in response:
        start_stop = route['startStop']
        end_stop = route['endStop']
        start_hour = route['startHour']
        end_hour = route['endHour']
        date = route['date']
        cost = route['cost']
        stops = []
        stops_json = route['stops']
        for stop in stops_json:
            stop_name = stop['name']
            stop_pos = stop['pos']
            stops.append(Stop(stop_name, stop_pos))
        user_routes.append(UserRoute(start_stop, end_stop, start_hour, end_hour, date, cost, stops))
    return user_routes
