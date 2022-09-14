from flask import Response
import json
from decimal import Decimal
import datetime

class response:

    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, datetime.datetime):
                return obj.__str__()
            return json.JSONEncoder.default(self, obj)

    def __init__(self, status=200, message="", data=None):
        result = { "status": status, "message": message, "data": data }
        self.body = json.dumps(result, cls=response.DecimalEncoder)

    def __str__(self): return self.body

    def get_json(self): return Response(self.body, mimetype="application/json")

    def get_html(self): return Response(self.body, mimetype="application/json")