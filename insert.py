# MIT Licensed. Copyright (c) 2017
import falcon

from sqlalchemy.orm import Session
from sqlalchemy import exists, and_
from database import engine, Base
from tables import UsersTable, SignaturesTable
from time import ctime

from utilities import getSignatureQuery, getJson, to_bool
from auth import authenticate

def recordUser(session, valueDict):
        userRow = None
        requiredValues = ["Signature", "Name", "Email", "UserID"]

        for value in requiredValues:
            if value not in valueDict.keys():
                return None
                #resp.body = "Error, missing key {}".format(value)
                #resp.status = falcon.HTTP_400

        # User table values
        signature = valueDict.get("Signature")
        name = valueDict.get("Name")
        email = valueDict.get("Email")
        company = valueDict.get("Company")
        userID = valueDict.get("UserID")

        userExists = True
        userRow = session.query(UsersTable).get((signature, userID))    

        if userRow is None:
            userExists = False
            userRow = UsersTable(Signature=signature, Name=name, Email=email, Company=company, UserID=userID, InstallDateTime=ctime())

        return userRow, userExists

def createSignatureRow(session, valueDict):
        signatureRow = None
        signature = valueDict.get("Signature")

        # Signature table values
        installLimit = valueDict.get("InstallLimit")
        unlimitedInstalls = to_bool(valueDict.get("UnlimitedInstalls"))

        if unlimitedInstalls is True:
            signatureRow = SignaturesTable(PrimaryKey=signature, InstallCount=0, InstallLimit=0, UnlimitedInstalls=unlimitedInstalls)
            print("Created Signature: {}, with UnlimitedInstalls".format(signature))
        elif installLimit is not None:
            signatureRow = SignaturesTable(PrimaryKey=signature, InstallCount=0, InstallLimit=installLimit, UnlimitedInstalls=False)
            print("Created Signature: {}, with InstallLimit of: {}".format(signature, installLimit))
        else:
            print("Error creating row with Signature: {}. No valid UnlimitedInstalls or InstallLimit provided".format(signature))

        return signatureRow

class Resource(object):

    def on_get(self, req, resp):
        resp.body = "Accepted!"
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        validRequest = authenticate(req)

        if not validRequest:
            resp.body = "Invalid username/password"
            resp.status = falcon.HTTP_401
            return

        session = Session(engine)
        valueDict = getJson(req)

        signatureQuery = getSignatureQuery(req, session)

        message = "Unable to add Signature"
        resp.status = falcon.HTTP_400

        if "Signature" in valueDict.keys() and signatureQuery is None:
            signatureRow = createSignatureRow(session, valueDict)
            message = "Unable to create signature row"
            if signatureRow is not None:
                session.add(signatureRow)
                message = "Added signature to database: {}".format(signatureRow.PrimaryKey)
                resp.status = falcon.HTTP_200

        elif "Signature" in valueDict.keys():
            message = "Unable to add Signature, already exists in database"

        resp.body = message
        print(message)

        session.commit()
        session.close()