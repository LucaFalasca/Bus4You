from flask import Flask, render_template, request, session, flash
import requests
from entity.User import User

app = Flask(__name__)
app.secret_key = '1234 bianchi legge questo e si sente male'


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html') #TODO aggiustare mettendo una navbar che porta alle varie pagine


@app.route('/login', methods=['POST'])
def login():
    mail = request.form.get('txtMail')
    pwd = request.form.get('txtPwd')
    print(mail)
    print(pwd)
    if mail == '' or pwd == '':
        flash('Login failed some required fields are empty')
        return render_template("login.html")
    else:
        gateway_login_url = 'http://localhost:50052/login?usr=' + mail + '&pwd=' + pwd
        response = requests.get(gateway_login_url).json()
        if response['message'] == 'Login successful':
            session['logged'] = True
            session['usr'] = mail.split('@')[0]
            session['mail'] = mail
            session['token'] = response['token']
            return render_template("loginSuccess.html")
        else:
            flash('Login failed incorrect mail or password')
            return render_template("loginFailed.html")



@app.route('/logout')
def logout():
    session.pop('logged', None)
    session.pop('usr', None)
    return render_template("logout.html")


@app.route('/signUp', methods=['POST'])
def signUp():
    name = request.form.get('txtName')
    surname = request.form.get('txtSurname')
    mail = request.form.get('txtMail')
    pwd = request.form.get('txtPwd')
    print(name)
    print(surname)
    print(mail)
    print(pwd)
    if name == '' or surname == '' or mail == '' or pwd == '':
        flash('Signup failed some required fields are empty')
        return render_template("signUp.html")
    else:
        gateway_sign_up_url = 'http://localhost:50052/signUp?name=' + name + '&surname=' + surname + '&usr=' + mail + '&pwd=' + pwd
        response = requests.get(gateway_sign_up_url).json()
        if response['message'] == 'Sign up successful':
            session['logged'] = True
            session['usr'] = mail.split('@')[0]
            session['mail'] = mail
            session['token'] = response['token']
            return render_template("signUpSuccess.html")
        else:
            flash('Signup failed')
            return render_template("signUpFailed.html")


if __name__ == '__main__':
    app.run(debug=True)
