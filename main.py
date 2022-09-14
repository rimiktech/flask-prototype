from flask import Flask, render_template, jsonify
import jinja2
import os

app = Flask(__name__)


from common.apidocs import apidocs
apidocs.register(app)


from common.loginmanager import LoginManager
LoginManager.views["login"] = "loginPage"
LoginManager.views["home"] = "home"
#@LoginManager.authorized




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


