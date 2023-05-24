class UserRoute:
    def __init__(self, start_stop, end_stop, start_hour, end_hour, date, cost, stops):
        self.startStop = start_stop
        self.endStop = end_stop
        self.startHour = start_hour
        self.endHour = end_hour
        self.date = date
        self.cost = cost
        self.stops = stops

    def getStartStop(self):
        return self.startStop

    def getEndStop(self):
        return self.endStop

    def getStartHour(self):
        return self.startHour

    def getEndHour(self):
        return self.endHour

    def getDate(self):
        return self.date

    def getCost(self):
        return self.cost

    def getStops(self):
        return self.stops
