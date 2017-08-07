# MIT Licensed. Copyright (c) 2017
import falcon
import json

from sqlalchemy.orm import Session
from database import engine, Base
from tables import *

from utilities import getSignatureQuery, getJson
from insert import recordUser

class Resource(object):

    def on_get(self, req, resp):
        resp.body = "Accepted!"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        session = Session(engine)        
        valueDict = getJson(req)
        signatureQuery = getSignatureQuery(req, session)

        signatureValid = False

        if signatureQuery:
            print("Found signature: {}".format(signatureQuery.PrimaryKey))

            userRow, userExists = recordUser(session, valueDict)
            availableSignature = signatureQuery.UnlimitedInstalls or signatureQuery.InstallCount <= signatureQuery.InstallLimit

            if userRow is not None and availableSignature:
                signatureValid = True
                
                # If the user didn't exist already we up the install count
                # If they did exist then we leave the install count as-is (probably did a reinstall)
                if not userExists:
                    signatureQuery.InstallCount = signatureQuery.InstallCount + 1

                session.add(userRow)
                print("Valid signature: Unlimited - {}, Install Count - {}, Existing User - {}".format(bool(signatureQuery.UnlimitedInstalls), signatureQuery.InstallCount, userExists))

        response = {'signatureValid': signatureValid}
        status = None
        if signatureValid:
            status = falcon.HTTP_200
        else:
            status = falcon.HTTP_400

        resp.body = json.dumps(response)
        resp.status = status
        
        session.commit()
        session.close()
