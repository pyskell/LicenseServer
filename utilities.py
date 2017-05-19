# MIT Licensed. Copyright (c) 2017
import json

from tables import *

def to_bool(value):

    if type(value) == bool:
        return value

    valid = {'true': True, 't': True, '1': True,
             'false': False, 'f': False, '0': False,}

    if not isinstance(value, str):
        return False # not a string so return false

    if value.lower() in valid:
        return valid[value.lower()]
    else:
        return False

def getJson(req):
    body = None

    if req.content_length != 0:
        req.stream.seek(0)
        data = req.stream.read(req.content_length or 0).decode('utf-8')
        body = json.loads(data)

    return body

def getSignatureQuery(req, session):
    clientIDQuery = None
    signatureQuery = None

    body = getJson(req)
        
    if "Signature" in body.keys():
        signature = body.get("Signature")

        if signature:
            print("Received Signature: {}".format(signature))
            signatureQuery = session.query(SignaturesTable).get(signature)

    return signatureQuery
