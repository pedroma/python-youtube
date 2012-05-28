"""
This modules create Python bindings for Youtube's API v2 using OAuth2.
Here is an example of how to use this module.

>>> client_id = "my-client-id" # get this from google's api console
>>> client_secret = "my-client-secret" # api console
>>> redirect_uri = "http://localhost/" # this has to be a registered URL in google's api console
>>> yt = YoutubeAPI(client_id, redirect_uri, client_secret)
>>> yt.get_auth_url() # send user to this url
>>> code = "code-provided-by-user"
>>> yt.finish_authorization(code)

At this point you have an authenticated instance of YoutubeAPI.
If you already have a credentials dictionary you can do:

>>> client_id = "my-client-id"
>>> client_secret = "my-client-secret"
>>> redirect_uri = "http://localhost/"
>>> credentials = {u'access_token': u'token-here', u'token_type': u'Bearer', u'expires_in': 3600, u'refresh_token': u'token-here'}
>>> yt = YoutubeAPI(client_id, redirect_uri, client_secret, credentials)

"""

import httplib, urllib, json, feedparser
from  models import YTUser, YTVideo

class YoutubeAPI(object):

    AUTH_URL_BASE = "https://accounts.google.com/o/oauth2/auth"
    API_BASE = "https://gdata.youtube.com"

    def __init__(self, client_id, redirect_uri, client_secret=None, credentials={}, scope = "http://gdata.youtube.com"):
        """
        client_secret optional for now. If its not set now we will need it later for the request token
        """
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.client_secret = client_secret
        self.credentials = credentials

    def get_auth_url(self):
        """
        Return the URL where the user should go to allow this application to manage their youtube account
        TODO: add an optional argument to add more GET parameters to request
        """
        return "%s?approval_prompt=force&access_type=offline&client_id=%s&redirect_uri=%s&response_type=code&scope=%s" % (self.AUTH_URL_BASE, self.client_id, self.redirect_uri, self.scope)

    def finish_authorization(self, code, client_secret=None):
        """
        Using the code provided by the authorization page send a request to get an authentication token.
        return a credentials dictionary with an access_token and a refresh_token
        store the refresh_token safely because any when we fetch a new token the refresh token will always be the same
        """
        if self.client_secret is None:
            if client_secret is None:
                raise Exception("You did not set a client_secret. Either pass it in this class's __init__ or in this method")
            else:
                self.client_secret = client_secret
        h1 = httplib.HTTPSConnection("accounts.google.com")
        params = urllib.urlencode({"client_id":self.client_id,"client_secret":self.client_secret,"redirect_uri":self.redirect_uri,"code":code,"grant_type":"authorization_code"})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        h1.request("POST","/o/oauth2/token",params,headers)
        resp = h1.getresponse()
        data = resp.read()
        self.credentials.update(json.loads(data))
        return self.credentials

    def refresh_token(self, credentials = None, client_secret=None):
        if self.client_secret is None:
            if client_secret is None:
                raise Exception("You did not set a client_secret. Either pass it in this class's __init__ or in this method")
            else:
                self.client_secret = client_secret
        if not self.credentials:
            if credentials is None:
                raise Exception("You did not set credentials. Either pass it in this class's __init__ or in this method")
            else:
                self.credentials = credentials
        h1 = httplib.HTTPSConnection("accounts.google.com")
        params = urllib.urlencode({"client_id":self.client_id,"client_secret":self.client_secret,"refresh_token":self.credentials['refresh_token'],"grant_type":"refresh_token"})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        h1.request("POST","/o/oauth2/token",params,headers)
        resp = h1.getresponse()
        data = resp.read()
        self.credentials.update(json.loads(data))
        return self.credentials

    def get_user_subscriptions(self):
        """
        This method assumes that the authorization process was complete and this class has a valid credentials dictionary.
        Return users subscriptions (not the actual subscription feed)
        """
        url = "%s/feeds/api/users/default/subscriptions?v=2&access_token=%s" % ( self.API_BASE, self.credentials['access_token'] )
        return feedparser.parse(url)


    def get_user_subscription_feed(self):
        """
        Return the user's subscription feed (videos)
        """
        url = "%s/feeds/api/users/default/newsubscriptionvideos?v=2&access_token=%s" % ( self.API_BASE, self.credentials['access_token'] )
        feed = feedparser.parse(url)
        if len(feed['items']):
            return [YTVideo(item) for item in feed['items']]

    def get_user_info(self, username="default"):
        """
        Returns a YTUser object with the user information. If no username is defined returns info for authenticated user
        """
        url = "%s/feeds/api/users/default?v=2&access_token=%s" % ( self.API_BASE, self.credentials['access_token'] )
        feed = feedparser.parse(url)
        if len(feed['items']):
            return YTUser(feed['items'][0])

