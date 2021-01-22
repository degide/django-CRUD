import jwt

SECRET = "123456"


def create_token(payload):
    return jwt.encode(payload, SECRET,  algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])
