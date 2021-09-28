#
#   This is a Python script to call the NIBE Uplink API which is protected by OAuth2 authentication
#   The necessary OAuth2 Token must have already been allocated and saved to a file called
#   .NIBE_Uplink_API_Token.json in the user's home directory
#
#   For more information see https://www.marshflattsfarm.org.uk/wordpress/?page_id=4988
#
#   Usage:
#       python3  simple_call_to_protected_api.py
#
#   Pre-requisites:
#     - A suitable OAuth2 Token must have already been allocated and saved to file
#
from os import path
from json import dump, load
from requests_oauthlib import OAuth2Session

HTTP_STATUS_OK = 200

#   The name of the file used to store the Token needs to be visible within the token_saver() function, so make it a Global Variable
home_dir = path.expanduser('~')
token_filename= home_dir + '/.NIBE_Uplink_API_Token.json'

#   Define a function that will be automatically called to save a new Token when it is refreshed
def token_saver(token):
    with open(token_filename, 'w') as token_file:
        dump(token, token_file)

#   Edit-in your own client_id and client_secret strings below
client_id = 'Replace this with the Identifier issued when your Application was registered' # (32 hex digits)
client_secret = 'Replace this with the Secret issued when your Application was registered' # (44 characters)

token_url = 'https://api.nibeuplink.com/oauth/token'

#   Read the previously-saved Token from file
with open(token_filename, 'r') as token_file:
    token = load(token_file)

#   Specify the list of extra arguments to include when refreshing a Token
extra_args = {'client_id': client_id, 'client_secret': client_secret}

#   Instantiate an OAuth2Session object (a subclass of Requests.Session) that will be used to query the API
#     - The default Client is of type WebApplicationClient, which is what we want; no need to specify that
#     - The 'client_id' was allocated when the Application was Registered
#     - The 'token' was allocated previously; read-in from a file
#     - The 'auto_refresh_url' says what URL to call to obtain a new Access Token using the Refresh Token
#     - The 'auto_refresh_kwargs' specifies which additional arguments need to be passed when refreshing a Token
#     - The 'token_updater' is the function that will persist the new Token whenever it is refreshed
nibeuplink = OAuth2Session(client_id=client_id, token=token, auto_refresh_url=token_url, auto_refresh_kwargs=extra_args, token_updater=token_saver)

#   Call the NIBE Uplink API - Get a list of the Systems assigned to the authorized user
response = nibeuplink.get('https://api.nibeuplink.com/api/v1/systems')
if response.status_code == HTTP_STATUS_OK:
    objects = response.json()['objects']
    print('Total of ' + str(objects['numItems']) + ' system(s) returned by the API query')
    for object in objects:
        print('System Id:   ' + object['systemId'])
        print('System Name: ' + object['name'])
else:
    print('HTTP Status: ' + str(response.status_code))
    print(response.text)
    raise SystemExit('API call not successful')
