#!/usr/bin/env python
import configparser
import fitbit
import os
import pprint
import sys
import webbrowser
from fitbit.api import FitbitOauthClient

FITBIT = 'FITBIT'

config = configparser.ConfigParser()
config.read('providers.ini')

print('config sections=',config.sections())

CLIENT_KEY = config[FITBIT]['client_key']
CLIENT_SECRET =  config[FITBIT]['client_secret']
ENCODED_USER_ID = config[FITBIT]['encoded_user_id']
OAUTH_TOKEN = config[FITBIT]['oauth_token']
OAUTH_TOKEN_SECRET = config[FITBIT]['oauth_token_secret']
#unauth_client = fitbit.Fitbit(CLIENT_KEY,CLIENT_SECRET)

# setup
pp = pprint.PrettyPrinter(indent=4)
print('** OAuth Python Library Example **\n')
client = FitbitOauthClient(CLIENT_KEY, CLIENT_SECRET)

authd_client = fitbit.Fitbit(CLIENT_KEY, CLIENT_SECRET, resource_owner_key=OAUTH_TOKEN, resource_owner_secret=OAUTH_TOKEN_SECRET)
print('activities=',authd_client.time_series('activities/steps',ENCODED_USER_ID,period='1d'))

exit(0)
# get request token
print('* Obtain a request token ...\n')
token = client.fetch_request_token()
print('RESPONSE')
pp.pprint(token)
print('')
print('* Authorize the request token in your browser\n')
stderr = os.dup(2)
os.close(2)
os.open(os.devnull, os.O_RDWR)
webbrowser.open(client.authorize_token_url())
os.dup2(stderr, 2)
try:
    verifier = raw_input('Verifier: ')
except NameError:
    # Python 3.x
    verifier = input('Verifier: ')
# get access token
print('\n* Obtain an access token ...\n')
token = client.fetch_access_token(verifier)
print('RESPONSE')
pp.pprint(token)
print('')
