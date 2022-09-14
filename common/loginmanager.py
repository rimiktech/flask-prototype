from collections import defaultdict
import urllib.parse
from flask import redirect, url_for, session, request, abort, jsonify, make_response

class LoginManager:
    views = { "login": "login", "home":  "home" }
    
    def get_current():
        return session.get("user")

    ''' Protect any url.'''
    def authorized(func, redirect=True):
        def inner(*args, **kwargs):
            user = session.get("user")
            if user is None and redirect:
                return LoginManager.__redirect_to_login()
            elif user is None:
                return make_response(jsonify({ "message": "Unathorized" }), 401)
            return func(*args, **kwargs)
        return inner

    ''' Login the user and redirect to home page '''
    def login(user, redirect=True):
        session["user"] = user
        if not redirect: return
        
        return_url = request.args.get("return")
        if return_url != "":
            url = urllib.parse.unquote(return_url)
            return redirect(url)
        return redirect(url_for(LoginManager.views["home"]))


    ''' logout the user and redirect to login page '''
    def logout(redirect=True):
        session.pop("user", None)
        if redirect:
            return url_for(LoginManager.views["login"])
        return

    ''' Redirect to login page or send unauthorized request. '''
    def __redirect_to_login():
        if LoginManager.login_view is None:
            abort(401) #abort the request as unauthenticated.
        
        url = url_for(LoginManager.views["login"]) + "?return=" + urllib.parse.quote(request.url)
        return redirect(url)