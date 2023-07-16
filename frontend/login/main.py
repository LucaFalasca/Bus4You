from datetime import datetime

from flask import Flask, render_template, request, session, flash, json, jsonify, redirect, url_for
import requests
from utils.json_parser import parse_user_routes_json

app = Flask(__name__)
app.secret_key = '1234 bianchi legge questo e si sente male'


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/signUpForm')
def signUpPage():
    return render_template('signUp.html')


@app.route('/login', methods=['POST'])
def login():
    mail = request.form.get('txtMail')
    pwd = request.form.get('txtPwd')
    if mail == '' or pwd == '':
        flash('Login failed some required fields are empty')
        return render_template("login.html")
    else:
        gateway_login_url = 'http://gateway-api:50052/api/login?usr=' + mail + '&pwd=' + pwd
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
        gateway_sign_up_url = 'http://gateway-api:50052/api/sign-up?name=' + name + '&surname=' + surname + '&mail=' + mail + '&pwd=' + pwd + '&usr=' + username + '&birthdate=' + birthdate
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
    start_lat = request.args.get('start_lat')
    start_lng = request.args.get('start_lng')
    ending_point = request.args.get('ending_point')
    end_lat = request.args.get('end_lat')
    end_lng = request.args.get('end_lng')
    date = request.args.get('date')
    start_or_finish_raw = request.args.get('start-finish')
    if start_or_finish_raw == 'on':
        start_or_finish = 'start'
    else:
        start_or_finish = 'finish'
    time = request.args.get('time')
    # print(starting_point)
    # print(ending_point)
    # print(date)
    # print(start_or_finish)
    # print(time)
    # print(start_lat)
    # print(start_lng)
    # print(end_lat)
    # print(end_lng)
    gateway_get_bus_stops_url = 'http://gateway-api:50052/api/get_bus_stops'
    bus_stops = requests.get(gateway_get_bus_stops_url).json()

    if starting_point is None or ending_point is None or date is None or start_or_finish is None or time is None or start_lat is None or start_lng is None or end_lat is None or end_lng is None:
        return render_template("select_route_from_map.html", bus_stops=bus_stops)
    else:
        gateway_request_route_url = 'http://gateway-api:50052/api/route-from-map?user=' + mail + '&starting_point=' + starting_point + '&start_lat=' + start_lat + '&start_lng=' + start_lng + '&ending_point=' + ending_point + '&end_lat=' + end_lat + '&end_lng=' + end_lng + '&date=' + date + '&start-finish=' + start_or_finish + '&time=' + time
        print(gateway_request_route_url)
        response = requests.get(gateway_request_route_url).json()
        session['user_routes'] = response
        return render_template("select_route_from_map.html", bus_stops=bus_stops, response=response)


@app.route('/_get_user_balance', methods=['GET'])
def get_user_balance():
    mail = session['mail']
    gateway_get_user_balance_url = 'http://gateway-api:50052/api/get_user_balance?user=' + mail
    balance = requests.get(gateway_get_user_balance_url).json()
    session['balance'] = balance
    return jsonify(result=balance)

@app.route('/load_recomended_routes_page', methods=['GET'])
def load_recomended_routes_page():
    usr = session['usr']
    mail = session['mail']
    gateway_get_recommended_routes_url = 'http://gateway-api:50052/api/get_future_confirmed_routes'
    recommended_routes = json.loads(requests.get(gateway_get_recommended_routes_url).json())
    
    #recommended_routes = ['Stringa 1', 'Stringa 2', 'Stringa 3', 'Stringa 4', 'Stringa 5', 'Stringa 6', 'Stringa 7', 'Stringa 8', 'Stringa 9', 'Stringa 10']
    return render_template("recommended_routes.html", recommended_routes=recommended_routes)


@app.route('/_get_stops_rect', methods=['GET'])
def get_stops_rect():
    x = request.args.get('x')
    y = request.args.get('y')
    height = request.args.get('height')
    width = request.args.get('width')
    gateway_get_bus_stops_url = 'http://gateway-api:50052/api/get_bus_stops_rect?x=' + x + '&y=' + y + '&height=' + height + '&width=' + width
    print(gateway_get_bus_stops_url)
    # print(requests.get(gateway_get_bus_stops_url))
    bus_stops = requests.get(gateway_get_bus_stops_url).json()
    return jsonify(result=bus_stops)


@app.route('/_get_path', methods=['POST'])
def get_path():
    data = request.get_json()
    print(data)

    url = 'http://gateway-api:50052/api/get_path'
    body = data

    result = requests.post(url, json=body).json()
    print(result)
    return jsonify(result=result)

@app.route('/_get_path_from_stops', methods=['POST'])
def get_path_from_stops():
    data = request.get_json()
    print(data)

    url = 'http://gateway-api:50052/api/get_path_from_stops'
    body = data

    result = requests.post(url, json=body).json()
    print(result)
    return jsonify(result=result)


@app.route('/loadUserRoutesPage', methods=['GET', 'POST'])
def load_user_routes_page():
    if session['logged']:
        usr = session['usr']
        mail = session['mail']
        # token = session['token']
        gateway_load_user_routes_url = 'http://gateway-api:50052/api/load_user_routes?mail=' + mail
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


@app.route('/reject_book', methods=['GET', 'POST'])
def reject_book():
    data = request.form
    parsed_data = []
    data_len = 0
    for elem in data.items():
        data_len += 1
        parsed_data.append([elem[0], elem[1]])
        # print("Key: \n\t" + elem[0])
        # print("Value: \n\t" + elem[1])

    # REJECT E RIMETTO IN CODA
    if data_len == 11:  # la submit non mette il valore della checkbox nella request solo se è spuntata quindi ho un parametro in più
        it_id = str(parsed_data[1][1])
        gateway_reject_book_url = 'http://gateway-api:50052/api/reject_it?it_id=' + it_id
        response = requests.get(gateway_reject_book_url).json()
        # print(response)
        if response['status'] == 'error':
            flash("Book rejection failed", category='info')
        elif response['status'] == 'ok':
            flash("Book rejected correctly", category='info')
            print("Rimetto in coda")
            gateway_requeue_url = 'http://gateway-api:50052/api/get_retry_info?it_id=' + it_id
            response = json.loads(requests.get(gateway_requeue_url).json())[0]
            mail = response[4]
            starting_point = response[9]
            start_lat = response[5]
            start_lng = response[6]
            ending_point = response[10]
            end_lat = response[7]
            end_lng = response[8]
            start_hour_tmp = response[0]
            finish_hour_tmp = response[1]
            date = ''
            time = ''
            start_or_finish = ''
            # costo_max = response[2] # not used
            # distanza = response[3] # not used
            if start_hour_tmp is None:
                start_or_finish = 'finish'
                it_prop_finish_obj = datetime.strptime(response[1], "%a, %d %b %Y %H:%M:%S %Z")
                finish_hour = it_prop_finish_obj.strftime("%Y-%m-%d %H:%M:%S")
                date = finish_hour.split(' ')[0]
                time = finish_hour.split(' ')[1]
            elif finish_hour_tmp is None:
                start_or_finish = 'start'
                it_prop_start_obj = datetime.strptime(response[0], "%a, %d %b %Y %H:%M:%S %Z")
                start_hour = it_prop_start_obj.strftime("%Y-%m-%d %H:%M:%S")
                date = start_hour.split(' ')[0]
                time = start_hour.split(' ')[1]
            print(mail)
            print(starting_point)
            print(start_lat)
            print(start_lng)
            print(ending_point)
            print(end_lat)
            print(end_lng)
            print(date)
            print(time)
            print(start_or_finish)
            gateway_request_route_url = 'http://gateway-api:50052/api/route-from-map?user=' + mail + '&starting_point=' + \
                                        starting_point + '&start_lat=' + start_lat + '&start_lng=' + start_lng + \
                                        '&ending_point=' + ending_point + '&end_lat=' + end_lat + '&end_lng=' + end_lng + \
                                        '&date=' + date + '&start-finish=' + start_or_finish + '&time=' + time
            print(gateway_request_route_url)
            response = requests.get(gateway_request_route_url).json()
            session['user_routes'] = response
            flash("Book requeued correctly", category='info')

    # NON RIMETTO IN CODA, SOLO REJECT
    else:
        print("Non rimetto in coda")
        it_id = str(parsed_data[0][1])
        gateway_reject_book_url = 'http://gateway-api:50052/api/reject_it?it_id=' + it_id
        response = requests.get(gateway_reject_book_url).json()
        # print(response)
        if response['status'] == 'ok':
            flash("Book rejected correctly, you will receive soon a refund", category='info')
        elif response['status'] == 'error':
            flash("Book rejection failed", category='info')

    return redirect(url_for('load_user_routes_page'))


@app.route('/confirm_book', methods=['GET', 'POST'])
def confirm_book():
    data = request.form
    parsed_data = []
    for elem in data.items():
        parsed_data.append([elem[0], elem[1]])
        # print("Key: \n\t" + elem[0])
        # print("Value: \n\t" + elem[1])
    it_id = parsed_data[0][1]
    gateway_confirm_book_url = 'http://gateway-api:50052/api/confirm_it?it_id=' + it_id
    response = requests.get(gateway_confirm_book_url).json()
    # print(response)
    if response['status'] == 'ok':
        flash("Book confirmed correctly", category='info')
    elif response['status'] == 'error':
        flash("Book confirmation failed", category='info')
    return redirect(url_for('load_user_routes_page'))

@app.route('/_get_total_km_trips', methods=['GET', 'POST'])
def get_total_km_trips():
    id_route = request.args.get('id')
    gateway_get_total_km_trips_url = 'http://gateway-api:50052/api/get_total_km?route_id=' + id_route
    print(gateway_get_total_km_trips_url)
    bus_stops = requests.get(gateway_get_total_km_trips_url).json()
    return jsonify(result=bus_stops)

@app.route('/_get_km_from_subroute', methods=['POST'])
def get_km_from_subroute():
    data = request.get_json()
    print(data)

    url = 'http://gateway-api:50052/api/get_km_from_subroute'
    body = data

    result = requests.post(url, json=body).json()
    print(result)
    return jsonify(result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
