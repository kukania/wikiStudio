from flask import Flask,render_template,send_from_directory,session
from wikiStudio.code.login import loginTask
from wikiStudio.code.insert import insert
from jinja2 import Environment,PackageLoader
from .code.makeTreeNav import makeTreeNav

env=Environment(loader=PackageLoader(__name__,'tmplates'))
app=Flask(__name__)
#app._static_folder=os.path.abspath("static/")
app.register_blueprint(loginTask)
app.register_blueprint(insert)
app.secret_key='cdb05b9f959af26e266b4c3ab5f09aca'
#session[nickname], sesseion[UID]
@app.route("/")
def showIndex():
    if 'nickname' in session:
        #print(session['nickname'])
        return render_template("example.html",session=session,treeNav=makeTreeNav(session),nickname=session['nickname'],contents="hello")
    else:
        return render_template("example.html")

@app.route("/static/<path:path>")
def staticRequest(path):
    print(path)
    return send_from_directory('static',path)
app.run()