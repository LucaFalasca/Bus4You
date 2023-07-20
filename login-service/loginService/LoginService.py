import hashlib
import xmlrpc.server

from dao.user_db.UserDbDao import UserDbDao


def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(('', 8000))
    print("Listening on port 8000...")

    server.register_function(rpc_login, "rpc_login")
    server.register_function(rpc_sign_up, "rpc_sign_up")
    server.serve_forever()


def rpc_login(mail, password):
    usr_db = UserDbDao()
    conn = usr_db.connect()
    log_ret = usr_db.login_query(conn, mail, password)
    conn.close()
    if log_ret == 0:
        print("Login successful")
        token = hashlib.md5((mail + password).encode('utf-8')).hexdigest()
        res = {"message": "Login successful", "token": token}
        return res
    else:
        res = {"message": "Login failed"}
        print("Login failed")
        return res


def rpc_sign_up(name, surname, mail, password, birthdate, username):
    usr_db = UserDbDao()
    conn = usr_db.connect()
    sign_up_ret = usr_db.sign_up(conn, name, surname, mail, password, birthdate, username)
    conn.close()
    if sign_up_ret == 0:
        print("Sign up successful")
        token = hashlib.md5((mail + password).encode('utf-8')).hexdigest()
        res = {"message": "Sign Up successful", "token": token}
        return res
    else:
        print("Sign up failed")
        res = {"message": "Sign Up failed"}
        return res


if __name__ == "__main__":
    serve()
