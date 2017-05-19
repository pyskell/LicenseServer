# MIT Licensed. Copyright (c) 2017
import sys

from sqlalchemy.orm import Session

from database import engine, Base
from tables import *

import random
from hashlib import sha256
from base64 import standard_b64decode

def authenticate(req):
    session = Session(engine)

    if req.content_length == 0:
        return False

    authrequest = standard_b64decode(req.auth.split(" ")[1]).split(b":")
    username = authrequest[0]

    if username is None:
        return False

    stored_user = session.query(AdminsTable).get(username)
    
    if stored_user is not None:
        stored_key = stored_user.Key.split("#")[0]
        salt = stored_user.Key.split("#")[1]

        key = authrequest[1].decode("utf-8") + salt
        key = key.encode("utf-8")
        key = sha256(key).hexdigest()

        return key == stored_key
    
    return False

    session.close()

def make_admin(username, key):

    session = Session(engine)
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    username = username.encode("utf-8")

    salt = ''.join(random.choice(ALPHABET) for i in range(16))
    key = key + salt

    encrypted_key = sha256(key.encode("utf-8")).hexdigest()
    encrypted_key = encrypted_key + "#" + salt

    newRow = AdminsTable(Username=username, Key=encrypted_key)

    session.add(newRow)

    session.commit()
    session.close()

if __name__ == '__main__':
    make_admin(sys.argv[1], sys.argv[2])