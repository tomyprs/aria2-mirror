# Why my "App isn't verified" ?
# This might returned by google APIs because
# we are using a high level scope here

# How to fix it ?
# Just hit the continue anyway button
# because here you are using you own credentials
# so no one gonna steal your data
# else
# complete your developer/app profile and
# submit for review and get verified
# W4RR10R

from oauth2client.client import OAuth2WebServerFlow
from bot.get_config import getConfig

__OAUTH_SCOPE = ['https://www.googleapis.com/auth/drive']
__REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

G_DRIVE_CLIENT_ID = getConfig("G_DRIVE_CLIENT_ID")
G_DRIVE_CLIENT_SECRET = getConfig("G_DRIVE_CLIENT_SECRET")

flow = OAuth2WebServerFlow(
    G_DRIVE_CLIENT_ID,
    G_DRIVE_CLIENT_SECRET,
    __OAUTH_SCOPE,
    redirect_uri=__REDIRECT_URI
)
auth_url = flow.step1_get_authorize_url()
print("Open this URL in any browser and get the refersh token: \n" + auth_url)
refresh_token = input("Enter the token: ")
auth = flow.step2_exchange(refresh_token).to_json()
print(auth)
