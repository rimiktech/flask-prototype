
from flask import url_for, jsonify
from urllib.parse import unquote

class apidocs:

    __instance = None

    def __get_endpoints(self):
        urls = []
        for rule in self.app.url_map.iter_rules():
            if rule.endpoint == "get_endpoints":
                continue
            
            args = { a: "<"+a+">" for a in rule.arguments }
            url = unquote(url_for(rule.endpoint, **args))
            urls.append({ "endpoint": url, "methods": list(rule.methods) })
        return jsonify(urls)

    def register(app):
        apidocs.__instance = apidocs()
        apidocs.__instance.app = app
        app.add_url_rule("/api.docs", view_func=apidocs.__instance.get_endpoints)
