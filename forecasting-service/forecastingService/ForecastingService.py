from datetime import datetime
import xmlrpc.client
import json
import requests

if __name__ == "__main__":
    bus = "Bus2"
    while(True):
        # Get the current date and time
        # current_datetime = datetime.datetime.now
        current_datetime = datetime(2023, 9, 16, 0, 5)
        # Extract and print the current time
        current_hour = current_datetime.time().hour
        current_minute = current_datetime.time().minute
        today_routes = []
        green_routes = []
        perc = 0.2
        kwh_cost = 0.118
        counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if current_hour == 0 and current_minute == 5:
            schedule = requests.get("http://193.206.108.146:33100/api/rec/scheduling?date=" + current_datetime.strftime(
                "%Y-%m-%d") + "&smartMeter=" + bus)
            schedule_json = json.loads(schedule.text)
            # Implementare il meccanismo di sconto basandosi sul forecasting
            forecasting_json = json.loads(requests.get("http://193.206.108.146:33100/api/rec/forecasting").text)
            forecasting = forecasting_json["produzione"]["values"]
            allocation = schedule_json["allocazione"]["values"]
            with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
                future_routes_info = json.loads(proxy.get_future_confirmed_routes())
            for elem in future_routes_info:
                date_object = datetime.strptime(elem[5], "%a, %d %b %Y %H:%M:%S GMT")
                if elem[1] == 1 and date_object.date() == current_datetime.date():
                    today_routes.append({"route_id": elem[0], "start": date_object.strftime("%Y-%m-%d %H:%M")})
                    # Mi guardo se l'allocazione corrispondente all'orario è true, in tal caso usa energia green e gli farò lo sconto
                    if allocation[date_object.strftime("%H")]:
                        index = allocation.index(allocation[date_object.strftime("%H")])
                        green_routes.append({"route_id": elem[0], "start": date_object.strftime("%Y-%m-%d %H:%M"),
                                             "index": index})
                        counter[index] += 1
            #Calcolo del cashback
            for elem in green_routes:
                cashback = (forecasting[elem["index"]]*perc*0.118)/counter[elem["index"]]
                with xmlrpc.client.ServerProxy("http://db-service:8000/") as proxy:
                    proxy.update_cashback(elem["route_id"], cashback)


        print(today_routes)
