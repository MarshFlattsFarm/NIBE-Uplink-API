#
#   This is a Python script to retrieve an OAuth2 Access Token for later use with the NIBE Uplink API
#   The allocated token is written to a file called .NIBE_Uplink_API_Token.json in the user's home directory
#
#   For more information see https://www.marshflattsfarm.org.uk/wordpress/?page_id=4988
#
#   Usage:
#       python3  request_token.py
#
#   Pre-requisites:
#     - The NIBE Uplink API website must have been used to register an Application (i.e. the script that will later call the API)
#     - The 'Identifier' and 'Secret' issued when the Application was registered must edited into the script below
#     - The 'redirect_url' must either be left as the default or you must be hosting an equivalent on your own HTTPS server
#
from os import path
from json import dump
from requests_oauthlib import OAuth2Session

#   Edit-in your own client_id and client_secret strings below
client_id = 'Replace this with the Identifier issued when your Application was registered' # (32 hex digits)
client_secret = 'Replace this with the Secret issued when your Application was registered' # (44 characters)

#   Change this if you are hosting your own Redirect URL (or leave as-is)
redirect_url = 'https://www.marshflattsfarm.org.uk/nibeuplink/oauth2callback/index.php'

query_scope = 'READSYSTEM'
unique_state = 'STATESTRING'
token_url = 'https://api.nibeuplink.com/oauth/token'
authorize_url = 'https://api.nibeuplink.com/oauth/authorize'

#   Instantiate an OAuth2Session object (a subclass of Requests.Session) that will be used to request the Token
#     - The default Client is of type WebApplicationClient, which is what we want; no need to specify that
#     - The 'client_id' was allocated when the Application was Registered
#     - The 'scope' is the type of permission we want to request (specfic to the API being called - either READSYSTEM or WRITESYSTEM here)
#     - The 'redirect_uri' is what we want to invoke as a call-back
#     - The 'state' is the secret string we specify when calling the Authorization URL
nibeuplink = OAuth2Session(client_id=client_id, scope=query_scope, redirect_uri=redirect_url, state=unique_state)

#   Tell the user which URL to browse to
print('Use a Web Browser to connect to:  ' + authorize_url + '?response_type=code&client_id=' + client_id + '&scope=' + query_scope + '&redirect_uri=' + redirect_url + '&state=' + unique_state)

#   Prompt the user to enter the Authorization Code returned by the Browser when they accessed the Authorization URL
authorization_code = input('Enter (copy-and-paste) the Authorization Code printed in the Web Browser:  ')

#   Check we did actually get a plausibly long code entered
if len(authorization_code) < 99:
    raise SystemExit('Invalid Authorization Code entered; exiting')

#   Request a Token from token_url, using the entered Code
token = nibeuplink.fetch_token(token_url=token_url, code=authorization_code, include_client_id=True, client_secret=client_secret)

#   Check that the Token looks sensible
if token['token_type'] != 'bearer':
    raise SystemExit('Invalid Token received; exiting')

#   Save the Token to a file
home_dir = path.expanduser('~')
token_filename = home_dir + '/.NIBE_Uplink_API_Token.json'
with open(token_filename, 'w') as token_file:
    dump(token, token_file)

#   All done
print('Token saved to file ' + token_filename)

