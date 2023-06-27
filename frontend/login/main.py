from flask import Flask, render_template, request, session, flash, json, jsonify, redirect, url_for
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
            return redirect(url_for('request_route'))
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
    usr = session['usr']
    mail = session['mail']
    starting_point = request.args.get('starting_point')
    ending_point = request.args.get('ending_point')
    date = request.args.get('date')
    start_or_finish_raw = request.args.get('start-finish')
    if(start_or_finish_raw == 'on'):
        start_or_finish = 'start'
    else:
        start_or_finish = 'finish'
    time = request.args.get('time')
    print(starting_point)
    print(ending_point)
    print(date)
    print(start_or_finish)
    print(time)
    gateway_get_bus_stops_url = 'http://localhost:50052/api/get_bus_stops'
    bus_stops = requests.get(gateway_get_bus_stops_url).json()
    if starting_point == None or ending_point == '' or date == '' or start_or_finish == '' or time == '':
        return render_template("select_route_from_map.html", bus_stops = bus_stops)
    else:
        gateway_request_route_url = 'http://localhost:50052/api/route-from-map?user='+mail+'&starting_point=' + starting_point + '&ending_point=' + ending_point + '&date=' + date + '&start-finish=' + start_or_finish + '&time=' + time
        print(gateway_request_route_url)
        response = requests.get(gateway_request_route_url).json()
        session['user_routes'] = response
        return render_template("select_route_from_map.html", bus_stops = bus_stops, response=response)


@app.route('/_get_stops_rect', methods=['GET'])
def get_stops_rect():
    x = request.args.get('x')
    y = request.args.get('y')
    height = request.args.get('height')
    width = request.args.get('width')
    gateway_get_bus_stops_url = 'http://localhost:50052/api/get_bus_stops_rect?x=' + x + '&y=' + y + '&height=' + height + '&width=' + width
    print("AOO")
    print(gateway_get_bus_stops_url)
    print(requests.get(gateway_get_bus_stops_url))
    bus_stops = requests.get(gateway_get_bus_stops_url).json()
    return jsonify(result = bus_stops)
    


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
        present_routes = []
        past_routes = []
        for elem in user_routes:
            if elem.isPast() == 1 or elem.getItStatus() == 'rejected':
                past_routes.append(elem)
            else:
                present_routes.append(elem)

        return render_template("userRoutes.html", past_routes=past_routes, present_routes=present_routes)

    else:
        flash('You have to be signed in to access this page')
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
