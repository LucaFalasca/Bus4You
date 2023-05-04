from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/performLogin', methods=['POST'])
def perform_login():
    mail = request.form.get('txtUsr')
    pwd = request.form.get('txtPwd')
    print(mail)
    print(pwd)
    gateway_login_url = 'http://localhost:50052/login?usr=' + mail + '&pwd=' + pwd
    response = requests.get(gateway_login_url).json()
    if response['message'] == 'Login successful':
        return render_template("loginSuccess.html")
    else:
        return render_template("loginFailed.html")


if __name__ == '__main__':
    app.run(debug=True)
