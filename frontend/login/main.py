from flask import Flask, render_template, request, session, flash
import requests
from frontend.login.utils.json_parser import parse_user_routes_json

app = Flask(__name__)
app.secret_key = '1234 bianchi legge questo e si sente male'


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/signUpForm')
def signUpPage():
    return render_template('signUp.html')

@app.route('/requestRoutePage')
def selectRouteFromMapPage():
    return render_template('select_route_from_map.html')


@app.route('/login', methods=['POST'])
def login():
    mail = request.form.get('txtMail')
    pwd = request.form.get('txtPwd')
    if mail == '' or pwd == '':
        flash('Login failed some required fields are empty')
        return render_template("login.html")
    else:
        gateway_login_url = 'http://localhost:50052/api/login?usr=' + mail + '&pwd=' + pwd
        response = requests.get(gateway_login_url).json()
        if response['message'] == 'Login successful':
            session['logged'] = True
            session['usr'] = mail.split('@')[0]
            session['mail'] = mail
            session['token'] = response['token']
            return request_route()
        else:
            flash('Login failed incorrect mail or password', category='info')
            return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('logged', None)
    session.pop('usr', None)
    flash("You have been logged out", category='info')
    return render_template("login.html")


@app.route('/signUp', methods=['POST'])
def signUp():
    name = request.form.get('txtName')
    surname = request.form.get('txtSurname')
    mail = request.form.get('txtMail')
    pwd = request.form.get('txtPwd')
    birthdate = request.form.get('txtDate')
    username = mail.split('@')[0]
    if name == '' or surname == '' or mail == '' or pwd == '' or birthdate == '':
        flash('Signup failed some required fields are empty')
        return render_template("signUp.html")
    else:
        gateway_sign_up_url = 'http://localhost:50052/api/sign-up?name=' + name + '&surname=' + surname + '&mail=' + mail + '&pwd=' + pwd + '&usr=' + username + '&birthdate=' + birthdate
        response = requests.get(gateway_sign_up_url).json()
        if response['message'] == 'Sign Up successful':
            flash('Sign Up successful now you can access with your credentials', category='info')
            return render_template("login.html")
        else:
            flash('Signup failed', category='info')
            return render_template("signUp.html")


@app.route('/select-route-from-map', methods=['GET'])
def request_route():
    starting_point = request.args.get('starting_point')
    ending_point = request.args.get('ending_point')
    date = request.args.get('date')
    arrival_time = request.args.get('arrival_time')
    travel_time = request.args.get('travel_time')
    print(starting_point)
    print(ending_point)
    print(date)
    print(arrival_time)
    print(travel_time)
    gateway_get_bus_stops_url = 'http://localhost:50052/api/get_bus_stops'
    bus_stops = requests.get(gateway_get_bus_stops_url).json()
    if starting_point == None or ending_point == '' or date == '' or arrival_time == '' or travel_time == '':
        return render_template("select_route_from_map.html", bus_stops = bus_stops)
    else:
        gateway_request_route_url = 'http://localhost:50052/api/route_from_map?starting_point=' + starting_point + '&ending_point=' + ending_point + '&date=' + date + '&arrival_time=' + arrival_time + '&travel_time=' + travel_time
        print(gateway_request_route_url)
        response = requests.get(gateway_request_route_url).json()
        session['user_routes'] = response
        return render_template("select_route_from_map.html", bus_stops = bus_stops, response=response)


@app.route('/loadUserRoutesPage', methods=['GET', 'POST'])
def load_user_routes_page():
    print('loadUserRoutesPage')
    if session['logged']:
        usr = session['usr']
        mail = session['mail']
        #token = session['token']
        gateway_load_user_routes_url = 'http://localhost:50052/api/load_user_routes?mail=' + mail
        response = requests.get(gateway_load_user_routes_url).json()
        user_routes = parse_user_routes_json(response)
        return render_template("userRoutes.html", user_routes=user_routes)

    else:
        flash('You have to be signed in to access this page')
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
