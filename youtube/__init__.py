import httplib, urllib, json, feedparser

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
        This method assumes that the authorization process was complete and this class has a valid credentials dictionary
        """
        url = "%s/feeds/api/users/default/subscriptions?v=2&access_token=%s" % ( self.API_BASE, self.credentials['access_token'] )

