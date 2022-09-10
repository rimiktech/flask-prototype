from flask import Flask, render_template, jsonify
import jinja2
import os
from common.apidocs import apidocs

app = Flask(__name__)

apidocs.register(app)

def render_template1(template, **context):
    template = os.path.split(template)
    path, template = template[0], template[1]
    
    environ = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=path))
    template = environ.get_template(template).render(context)
    return template

@app.route('/')
def front_home():
    return render_template1("frontend/templates/index.html")

@app.route('/admin/<userid>')
def admin_home():
    return render_template1("admin/templates/index.html")

if __name__ == '__main__':
    app.run(debug=True)


