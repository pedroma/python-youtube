python-youtube
==============

Youtube python bindings for v2 using OAuth2

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
