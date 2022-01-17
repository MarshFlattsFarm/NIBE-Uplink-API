#
#   This is a Python script to call the NIBE Uplink API which is protected by OAuth2 authentication
#   The necessary OAuth2 Token must have already been allocated and saved to a file called
#   .NIBE_Uplink_API_Token.json in the user's home directory
#
#   For more information see https://www.marshflattsfarm.org.uk/wordpress/?page_id=4988
#
#   Usage:
#       python3  get_parameters_for_categories_for_systems.py
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
#   Documentation for this API call is at: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems_page_itemsPerPage
response = nibeuplink.get('https://api.nibeuplink.com/api/v1/systems')
if response.status_code != HTTP_STATUS_OK:
    print('HTTP Status: ' + str(response.status_code))
    print(response.text)
    raise SystemExit('API call not successful')

#   The array of Systems is tagged as 'objects' in the JSON output
systems = response.json()['objects']

for system in systems:
    system_id = system['systemId']
    print('System Id:  ' +  str(system_id))

    #   Call the NIBE Uplink API - Get the list of Units connected to this System (i.e. the Master and any Slave Units)
    #   Documentation for this API call is at: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-units
    response = nibeuplink.get('https://api.nibeuplink.com/api/v1/systems/' + str(system_id) + '/units')
    if response.status_code != HTTP_STATUS_OK:
        print('HTTP Status: ' + str(response.status_code))
        print(response.text)
        raise SystemExit('API call not successful')
    
    #   The JSON output is an Array of Units
    units = response.json()

    for unit in units:
        unit_id = unit['systemUnitId']
        print('\tUnit Id:  ', unit_id)

        #   The Unit ID needs to be supplied as an HTTP Parameter in subsequent API calls
        params = {'systemUnitId': unit_id}

        #   Call the NIBE Uplink API - Get the list of parameter Categories defined for this System
        #   Documentation for this API call is at: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-serviceinfo-categories_systemUnitId_parameters
        response = nibeuplink.get('https://api.nibeuplink.com/api/v1/systems/' + str(system_id) + '/serviceinfo/categories', params=params)
        if response.status_code != HTTP_STATUS_OK:
            print('HTTP Status: ' + str(response.status_code))
            print(response.text)
            raise SystemExit('API call not successful')
        
        #   The JSON output is simply an array of Categories
        categories = response.json()

        for category in categories:
            category_id = category['categoryId']
            print('\t\tCategory Id:  ', category_id)

            #   Call the NIBE Uplink API - Get the Parameters for this Category
            #   Documentation for this API call is at: https://api.nibeuplink.com/docs/v1/Api/GET-api-v1-systems-systemId-serviceinfo-categories-categoryId_systemUnitId
            response = nibeuplink.get('https://api.nibeuplink.com/api/v1/systems/' + str(system_id) + '/serviceinfo/categories/' + str(category_id), params=params)
            if response.status_code != HTTP_STATUS_OK:
                print('HTTP Status: ' + str(response.status_code))
                print(response.text)
                raise SystemExit('API call not successful')
            
            #   The JSON output is simply an array of Parameters
            parameters = response.json()
            
            for parameter in parameters:
                parameter_id = parameter['parameterId']
                parameter_name = parameter['name']
                parameter_title = parameter['title']
                parameter_designation = parameter['designation']
                parameter_unit = parameter['unit']
                parameter_display_value = parameter['displayValue']
                parameter_raw_value = parameter['rawValue']
                print('\t\t\tParameter Id:              ' + str(parameter_id))
                print('\t\t\t\tParameter Name:          ' + str(parameter_name))
                print('\t\t\t\tParameter Title:         ' + str(parameter_title))
                print('\t\t\t\tParameter Designation:   ' + str(parameter_designation))
                print('\t\t\t\tParameter Unit:          ' + str(parameter_unit))
                print('\t\t\t\tParameter Display Value: ' + str(parameter_display_value))
                print('\t\t\t\tParameter Raw Value:     ' + str(parameter_raw_value))
