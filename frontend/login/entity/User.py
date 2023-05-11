class User:
    def __init__(self, mail, username, token):
        self.mail = mail
        self.username = username
        self.token = token

    def get_mail(self):
        return self.mail
    def get_username(self):
        return self.username
    def get_token(self):
        return self.token