import os
import pathlib
import time
import globus_sdk
import numpy as np

from gdauth import log


__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2024, UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['refresh_globus_token',
           'create_clients',
           'create_dir',
           'check_folder_exists',
           'get_user_id',
           'share',
           'find_endpoints',
           'create_folder_link',
           'create_links',
           'find_endpoint_uuid',
           'find_items'
           ]


def refresh_globus_token(app_uuid):
    """
    Verify that existing Globus token exists and it is still valid, 
    if not creates & saves or refresh & save the globus token. 
    The token is valid for 48h.

    Parameters
    ----------
    app_uuid : App UUID 

    Returns
    -------
    ac, tc tokens : string
    """

    globus_token_file=os.path.join(str(pathlib.Path.home()), 'token.npy')

    try:
        token_response = np.load(globus_token_file, allow_pickle='TRUE').item()
    except FileNotFoundError:
        log.error('Globus token is missing. Creating one')
        # Creating new token
        # --------------------------------------------
        client = globus_sdk.NativeAppAuthClient(app_uuid)
        client.oauth2_start_flow(refresh_tokens=True)

        log.error('Please go to this URL and login:')
        log.warning('{0}'.format(client.oauth2_get_authorize_url()))

        get_input = getattr(__builtins__, 'raw_input', input)
        auth_code = get_input('Please enter the code you get after login here: ').strip() # pythn 3
        # auth_code = raw_input('Please enter the code you get after login here: ').strip() # python 2.7
        token_response = client.oauth2_exchange_code_for_tokens(auth_code)
        # --------------------------------------------
        np.save(globus_token_file, token_response) 

    # let's get stuff for the Globus Transfer service
    globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
    # the refresh token and access token, often abbr. as RT and AT
    transfer_rt = globus_transfer_data['refresh_token']
    transfer_at = globus_transfer_data['access_token']
    expires_at_s = globus_transfer_data['expires_at_seconds']

    globus_token_life = expires_at_s - time.time()
    if (globus_token_life < 0):
        # Creating new token
        # --------------------------------------------
        globus_app_id = app_uuid
        client = globus_sdk.NativeAppAuthClient(globus_app_id)
        client.oauth2_start_flow(refresh_tokens=True)

        log.error('Please go to this URL and login:')
        log.warning('{0}'.format(client.oauth2_get_authorize_url()))

        get_input = getattr(__builtins__, 'raw_input', input)
        auth_code = get_input('Please enter the code you get after login here: ').strip()
        token_response = client.oauth2_exchange_code_for_tokens(auth_code)
        # --------------------------------------------
        np.save(globus_token_file, token_response) 

    return token_response


def create_clients(app_uuid):
    """
    Create authorize and transfer clients

    Parameters
    ----------
    globus_app_id : App UUID 

    Returns
    -------
    ac : Authorize client
    tc : Transfer client
      
    """

    token_response = refresh_globus_token(app_uuid)
    print('***************')
    print('***************')
    print(token_response)
    print('***************')
    print('***************')
    # let's get stuff for the Globus Transfer service
    globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
    # the refresh token and access token, often abbr. as RT and AT
    transfer_rt = globus_transfer_data['refresh_token']
    transfer_at = globus_transfer_data['access_token']
    expires_at_s = globus_transfer_data['expires_at_seconds']

    globus_token_life = expires_at_s - time.time()
    log.info("Globus access token will expire in %2.2f hours", (globus_token_life/3600))

    client = globus_sdk.NativeAppAuthClient(app_uuid)
    client.oauth2_start_flow(refresh_tokens=True)
    # Now we've got the data we need we set the authorizer
    authorizer = globus_sdk.RefreshTokenAuthorizer(transfer_rt, client, access_token=transfer_at, expires_at=expires_at_s)

    ac = globus_sdk.AuthClient(authorizer=authorizer)
    tc = globus_sdk.TransferClient(authorizer=authorizer)

    return ac, tc


def create_dir(directory, # Directory to be created in the share
               app_uuid,  # Globus App / Client UUID
               ep_uuid):  # Endpoint UUID
    """
    Create directory

    Parameters
    ----------
    directory  : Directory to be created in the share
    app_uuid   : Globus App / Client UUID
    ep_uuid    : Endpoint UUID

    Returns
    -------
    Boolean : True if directory is created
      
    """

    dir_path = str(directory) + '/'
    ac, tc = create_clients(app_uuid)
    try:
        response = tc.operation_mkdir(ep_uuid, path=dir_path)
        log.info('*** Created folder: %s' % dir_path)
        log.warning(create_folder_link(directory, app_uuid, ep_uuid))
        return True
    except globus_sdk.TransferAPIError as e:
        log.warning(f"Transfer API Error: {e.code} - {e.message}")
        log.warning(create_folder_link(directory, app_uuid, ep_uuid))
        # log.error(f"Details: {e.raw_text}")
        return True
    except:
        log.error('*** Unknow error')
        return False


def check_folder_exists(directory, app_uuid, ep_uuid):
    """
    Check if directory exists
    
    Parameters
    ----------
    directory  : Directory to be created in the share
    app_uuid   : Globus App / Client UUID
    ep_uuid    : Endpoint UUID

    Returns
    -------
    Boolean : True if directory exists  
    """

    ac, tc = create_clients(app_uuid)

    try:
        tc.operation_ls(ep_uuid, path=directory)
        return True
    except globus_sdk.TransferAPIError as e:
        if e.code == 'ClientError.NotFound':
            return False
        else:
            raise e


def get_user_id(app_uuid, email):
    """
    Get user id from user email
    
    Parameters
    ----------
    app_uuid   : Globus App / Client UUID
    email      : User email address

    Returns
    -------
    string : User ID
      
    """

    ac, tc = create_clients(app_uuid)

    
    try:
        r = ac.get_identities(usernames=email, provision=True)
        user_id = r['identities'][0]['id']
        return user_id
    except globus_sdk.AuthAPIError as e:
        if e.code == 'MISSING_PARAMETERS':
            log.error(f"Authorization API Error: {e.code} - {e.message}")
            return None
        else:
            raise e

def share(directory,       # Name of the directory to share
          email,           # Email address to share the Globus directory with
          app_uuid,        # Globus App UUID
          ep_uuid,         # Endpoint UUID
          message=''       # Custom message to include to the email
          ):         
    """
    Share an existing globus directory with a Globus user. The user receives an email with the link to the folder.
    To add a custom message to the email edit the "notify message" field below
 
    Parameters
    ----------
    directory   : Name of the directory to share
    email       : Email address to share the Globus directory with
    app_uuid    : Globus App UUID
    ep_uuid     : Endpoint UUID

    Returns
    -------
    Boolean : True if folder is shared
    """


    if check_folder_exists(directory, app_uuid, ep_uuid):
        ac, tc = create_clients(app_uuid)
        user_id = get_user_id(app_uuid, email)
        if user_id != None:
            dir_path = '/' + str(directory) + '/'
            # Set access control and notify user
            rule_data = {
              'DATA_TYPE': 'access',
              'principal_type': 'identity',
              'principal': user_id,
              'path': dir_path,
              'permissions': 'r',
              'notify_email': message,
              'notify_message': "add here a custom meassage"
            }

            try: 
                response = tc.add_endpoint_acl_rule(ep_uuid, rule_data)
                log.info('*** Path %s has been shared with %s' % (dir_path, email))
                log.warning(create_folder_link(directory, app_uuid, ep_uuid))
                return True
            except globus_sdk.TransferAPIError as e:
                if (e.code == 'Exists'):
                    log.error(f"Transfer API Error: {e.code} - {e.message}")
                    log.warning(create_folder_link(directory, app_uuid, ep_uuid))
                    return True
                else:
                    return False
        else:
            log.error('Invalid user id')
    else:
        log.error('Directory does not exist')
        log.error('Create: %s' % directory)


def find_endpoints(app_uuid):
    """
    Find all end points

    Parameters
    ----------
    app_uuid    : Globus App UUID

    Returns
    -------
    dictionary : {endpoint name : endpoint id}
    """

    ac, tc = create_clients(app_uuid)
    
    my_endpoints ={}
    endpoints_shared_with_me = {}
    endpoints_shared_by_me = {}

    for ep in tc.endpoint_search(filter_scope="my-endpoints"):
        my_endpoints[ep['display_name']] = ep['id']
    for ep in tc.endpoint_search(filter_scope="shared-with-me"):
        endpoints_shared_with_me[ep['display_name']] = ep['id']
    for ep in tc.endpoint_search(filter_scope="shared-by-me"):
        endpoints_shared_by_me[ep['display_name']] = ep['id']

    return  my_endpoints, endpoints_shared_with_me, endpoints_shared_by_me


def create_folder_link(directory, app_uuid, ep_uuid):
    """
    Create link to a shared folder

    Parameters
    ----------
    directory   : Name of the directory to share
    app_uuid    : Globus App UUID
    ep_uuid     : Endpoint UUID

    Returns
    -------
    string : folder url
    """

    ac, tc = create_clients(app_uuid)

    url = 'https://app.globus.org/file-manager?&origin_id='+ep_uuid+'&origin_path=/'+str(directory) #+'/&add_identity='+user_id

    return url


def create_links(directory, app_uuid, ep_uuid, show=False):
    """
    Create the links for all items (folder and files) listed in the endpoint directory

    Parameters
    ----------
    directory   : Name of the directory to share
    app_uuid    : Globus App UUID
    ep_uuid     : Endpoint UUID

    Returns
    -------
    lists : [file url],  [folder url]
    """

    file_links   = []
    folder_links = []

    ac, tc = create_clients(app_uuid)
    files, folders  = find_items(directory, app_uuid, ep_uuid)

    for file_name in files:
        file_link = 'https://' + tc.get_endpoint(ep_uuid)['tlsftp_server'][9:-4] + '/' + str(directory) + '/' + file_name
        file_links.append(file_link)

    for folder in folders:            
        folder_link = 'https://app.globus.org/file-manager?&origin_id=' + ep_uuid + '&origin_path=' + str(directory) + '/' + folder #+'/&add_identity='+user_id
        folder_links.append(folder_link)
        if folder[-4:] == 'zarr':
            file_link = 'https://' + tc.get_endpoint(ep_uuid)['tlsftp_server'][9:-4] + '/' + str(directory) + '/' + folder
            file_links.append(file_link)

    return file_links, folder_links


def find_endpoint_uuid(app_uuid, ep_name):
    """
    Find end point UUID

    Parameters
    ----------
    app_uuid    : Globus App UUID
    ep_name     : Endpoint name

    Returns
    -------
    String : endpoin UUID
    """
    ep_uuid = None
    # Ask the Globus server to show all end points it has access to

    my_endpoints, endpoints_shared_with_me, endpoints_shared_by_me = find_endpoints(app_uuid)
    if ep_name in my_endpoints:
        ep_uuid = my_endpoints[ep_name]
    elif ep_name in endpoints_shared_with_me:
        ep_uuid = endpoints_shared_with_me[ep_name]
    elif ep_name in endpoints_shared_by_me:
        ep_uuid = endpoints_shared_by_me[ep_name]
    else:
        log.error('%s endpoint does not exists' % ep_name)
        log.error('Select one of this endpoints:')
        for key, value in my_endpoints.items():
            log.error('*** *** %s' % key)
        for key, value in endpoints_shared_with_me.items():
            log.error('*** *** %s' % key)
        for key, value in endpoints_shared_by_me.items():
            log.error('*** *** %s' % key)

    return ep_uuid



            # try: 
            #     response = tc.add_endpoint_acl_rule(ep_uuid, rule_data)
            #     log.info('*** Path %s has been shared with %s' % (dir_path, email))
            #     log.warning(create_folder_link(directory, app_uuid, ep_uuid))
            #     return True
            # except globus_sdk.TransferAPIError as e:
            #     if (e.code == 'Exists'):
            #         log.error(f"Transfer API Error: {e.code} - {e.message}")
            #         log.warning(create_folder_link(directory, app_uuid, ep_uuid))
            #         return True
            #     else:
            #         return False

def find_items(directory, app_uuid, ep_uuid):
    """
    Find items (file or folders) present in the directory

    Parameters
    ----------
    directory   : Name of the directory to share
    app_uuid    : Globus App UUID
    ep_uuid     : Endpoint UUID

    Returns
    -------
    Lists : [files], [folders]
    """

    ac, tc = create_clients(app_uuid)
    files   = []
    folders = []
    try:
        response = tc.operation_ls(ep_uuid, path=directory)
        for item in response['DATA']:
            log.info('directory %s contains %s: %s' % (directory, item['type'], item['name']))
            if item['type'] == 'file':
                files.append(item['name'])
            if item['type'] == 'dir':
                folders.append(item['name'])
    except globus_sdk.TransferAPIError as e:
        log.error(f"Transfer API Error: {e.code} - {e.message}")

    return files, folders
