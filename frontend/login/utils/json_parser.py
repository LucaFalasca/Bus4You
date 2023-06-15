from datetime import datetime

from frontend.login.entity.user_route import UserRoute


def parse_user_routes_json(response):
    user_routes = []
    for route in response:
        it_cost = route['it_cost']
        tmp_it_prop_start = route['it_prop_start']
        tmp_it_prop_end = route['it_prop_end']
        it_status = route['it_status']
        route_past = route['route_past']
        route_status = route['route_status']
        tmp_route_expire = route['route_expire']
        start_stop = route['start_stop']
        end_stop = route['end_stop']
        it_prop_start_obj = datetime.strptime(tmp_it_prop_start, "%a, %d %b %Y %H:%M:%S %Z")
        it_prop_start = it_prop_start_obj.strftime("%d/%m/%Y %H:%M:%S")
        it_prop_end_obj = datetime.strptime(tmp_it_prop_end, "%a, %d %b %Y %H:%M:%S %Z")
        it_prop_end = it_prop_end_obj.strftime("%d/%m/%Y %H:%M:%S")
        route_expire_obj = datetime.strptime(tmp_route_expire, "%a, %d %b %Y %H:%M:%S %Z")
        route_expire = route_expire_obj.strftime("%d/%m/%Y %H:%M:%S")
        user_routes.append(UserRoute(it_cost, it_prop_start, it_prop_end, it_status, route_past, route_status,
                                     route_expire, start_stop, end_stop))
    return user_routes
