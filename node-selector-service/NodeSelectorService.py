import requests

gateway_login_url = 'http://ors-app:8080/ors/v2/directions/driving-car?start=12.527504,41.837339&end=12.611618,41.853708'
response = requests.get(gateway_login_url).json()
print(response)


