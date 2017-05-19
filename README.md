# Purpose
This daemon allows for license management by simply keeping a record of license signatures and how many times they are allowed to be used (1, 2..unlimited).
It does no formal verification of signatures so any program you use this with will still need to verify the signature.

This is simply a secondary safety to prevent people from sharing their license keys with others (unless you allow them to do so). You can also revoke signatures (by setting their InstallLimit to 0)

Originally developed to be used with Portable.Licensing although the layout is so simple it should work with any licensing software that can provide a Signature and a reasonably unique UserID/HardwareID type of identifier.

# Configuration
1. Run `python auth.py USERNAME PASSWORD` to create a new administrator user. This user will be allowed to insert Signatures into the database via the `/insert` endpoint, using Basic Auth headers.
1. Run `python make_db.py` to create the SQLite3 database.
1. To run it in dev mode you can run `python app.py dev`, and for production/live mode run `python app.py live`

Dev mode runs on port 8080 by default and logs errors to stdout.

Live mode runs on port 9090 and logs errors to a log file. Though this appears broken at the moment so best to log stdout to a file via: `python app.py live >> stdout 2>&1 &`

# Usage
This is a RESTful application so send your requests via HTTP Post with a JSON string as the body.

You can use endpoints such as `http://HOSTNAME:PORT/ENDPOINT` but it's suggested to use `http://HOSTNAME:PORT/licenseserver/v1/ENDPOINT` in case future versions change the protocol.

### /insert
Insert a new signature and define its allowed usage.

Requires HTTP Basic Auth headers that match an admin user which you setup previously.

The JSON request must contain a Signature (string), and one of InstallLimit (int), or UnlimitedInstalls (bool)

If UnlimitedInstalls isn't specified then it's assumed to be false by the server.

Example that limits a Signature to 2 uses:

```
{"Signature": "YOURSIGNATURE",
 "InstallLimit" : "2"}
```

And one that allows unlimited Signature usage (such as for trials):
```
{"Signature": "YOURSIGNATURE",
 "UnlimitedInstalls" : "True"}
```

Trying to insert a signature which already exists will result in the program ignoring the addition and returning an error code. If you need to do this at the moment then it's best to open the database on the server with `sqlite3` and make your adjustments manually.

### /validate
Asks the server if a given Signature is valid and records information about the user validating the signature.

If the Signature is valid then it will record the User's UserID (which should be a reasonably unique ID), Name, Email, Company (optional), the date/time of install, and the validated signature. 

Example request:

```
{"Signature":"YOURSIGNATURE",
"Name":"Max",
"Email":"max@steel.com",
"UserID":"0xfe5712d89a"}
```

Example response:
```
{"signatureValid":"True"}
```

On the first request the new User will be stored in the User table, and the Signature's InstallCount will be incremented by 1. On subsequent requests, if there's a User with matching Signature and UserID then the User's "InstallDateTime" entry will be updated but no further change will be made to the Signature's InstallCount.

### UserIDs
UserIDs are entirely up to you, this program will accept any string and makes no attempt to validate the ID. Pick your ID according to exactly how reliable you need it to be.

You should also hash the IDs before sending them out.

# Note
Don't expect too many updates to this software as I'm self-employed and don't have too much free time to dedicate to adding functionality that I don't need. However, I am very happy to merge commits which fix bugs and add functionality.

# MIT License
Copyright 2017

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
OR OTHER DEALINGS IN THE SOFTWARE.