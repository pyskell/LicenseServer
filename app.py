# MIT Licensed. Copyright (c) 2017
import falcon
import validate
import insert
import sys

from waitress import serve
import logging

api = application = falcon.API()

validate = validate.Resource()
api.add_route('/validate', validate)

insert = insert.Resource()
api.add_route('/insert', insert)

if __name__ == '__main__':    

    if sys.argv[1] == 'live':
        # TODO: Logging may not actually be working right
        logger = logging.getLogger('waitress')
        logfile = logging.FileHandler('license_server.log')
        logger.setLevel(logging.WARN)
        logger.addHandler(logfile)

        serve(api, url_prefix='licenseserver/v1', listen='*:9090')
    else:
        serve(api, url_prefix='licenseserver/v1', listen='*:8080')