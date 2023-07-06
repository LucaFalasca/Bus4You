class UserRoute:
    def __init__(self, it_id, it_cost, it_prop_start, it_prop_end, it_status, route_past, routet_status,
                 route_expire, start_stop, end_stop):
        self.it_id = it_id
        self.itCost = it_cost
        self.itPropStart = it_prop_start
        self.itPropEnd = it_prop_end
        self.itStatus = it_status
        self.routePast = route_past
        self.routeStatus = routet_status
        self.routeExpire = route_expire
        self.startStop = start_stop
        self.endStop = end_stop

    def getItId(self):
        return self.it_id

    def getItCost(self):
        return self.itCost

    def getItPropStart(self):
        return self.itPropStart

    def getItPropEnd(self):
        return self.itPropEnd

    def getItStatus(self):
        return self.itStatus

    def isPast(self):
        return self.routePast

    def getRouteStatus(self):
        return self.routeStatus

    def getRouteExpire(self):
        return self.routeExpire

    def getStartStop(self):
        return self.startStop

    def getEndStop(self):
        return self.endStop
