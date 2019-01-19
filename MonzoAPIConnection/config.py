# Register your third party application on http://developers.monzo.com by logging in with your personal 
# Monzo account. Copy this file into config.py, and enter your credentials into the file.
MONZO_CLIENT_ID = "oauth2client_00009exSlmW1N1e2FvtE5R"
MONZO_CLIENT_SECRET = "mnzconf.6tEw/oPZQjn+SfNSsWg8E9HMBEvOhpZ/sxTmYl+FCiRIcshruHr7DU/8GHOUyz7zo2+xjE1rqgvfgFegfHPx"

# Configurations you should not need to change.
MONZO_OAUTH_HOSTNAME = "auth.monzo.com"
MONZO_API_HOSTNAME = "api.monzo.com"
MONZO_RESPONSE_TYPE = "code"
MONZO_AUTH_GRANT_TYPE = "authorization_code"
MONZO_REFRESH_GRANT_TYPE = "refresh_token"
MONZO_OAUTH_REDIRECT_URI = "http://127.0.0.1:21234/" # For receiving the auth code, not currently used.
MONZO_CLIENT_IS_CONFIDENTIAL = True 
# If your application runs on a backend server with client secret hidden from user, it should be registered 
# as confidential and will have the ability to refresh access tokens.
