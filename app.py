from flask import Flask

from loginService.dao.user_db import UserDbDao as usrDb

app = Flask(__name__)


def login(conn, username, password):
    usr_db_curs = conn.cursor()
    args = (username, password)
    usr_db_curs.callproc('services', args)
    res = []
    for result in usr_db_curs.stored_results():
        res.append(result.fetchall())
    if len(res) > 0:
        return 0
    else:
        return 1


@app.route('/')
def prova():
    usr_db = usrDb.UserDbDao()
    conn = usr_db.connect()
    if conn is not None:
        # print("Connection successful")
        log_res = login(conn, 'prova', '1234')
        conn.close()
        if log_res == 0:
            return "Login successful"
        else:
            return "Login failed"
    else:
        return "Connection failed"


'''if __name__ == "__main__":
    usr_db = usrDb.UserDbDao('localhost', 'b4y_userdb', 'root', 'root')
    conn = usr_db.connect()
    if conn is not None:
        print("Connection successful")
        log_res=services(conn, 'prova', '1234')
        if log_res==0:
            print("Login successful")
        else:
            print("Login failed")
        conn.close()
    else:
        print("F bro")'''
