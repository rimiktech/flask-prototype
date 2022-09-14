'''
We have a flask plugin which list out all urls created in flask app.
It exposes a url "apio.docs" which returns the list of all urls created in flask app.

Right now it returns the relative url, http verbs only. Please modify this code to return the comments of urls.
'''

from flask import url_for, jsonify
from urllib.parse import unquote

class apidocs:

    __instance = None

    def __get_defination(self, endpoint):
        ref = None
        for name, func in self.app.view_functions.items():
            if name == endpoint:
                ref = func
                break
        return ref.__doc__ if ref is not None else None
    
    def __get_endpoints(self):
        urls = []
        for rule in self.app.url_map.iter_rules():
            if rule.endpoint == "__get_endpoints":
                continue

            args = { a: "<"+a+">" for a in rule.arguments }
            url = unquote(url_for(rule.endpoint, **args))
            comment = self.__get_defination(rule.endpoint)
            urls.append({ "endpoint": url, "methods": list(rule.methods), "comment": comment })
        return jsonify(urls)

    def register(app):
        apidocs.__instance = apidocs()
        apidocs.__instance.app = app
        app.add_url_rule("/api.docs", view_func=apidocs.__instance.__get_endpoints)
