from flask import Flask,render_template,send_from_directory
import os
app=Flask(__name__)
#app._static_folder=os.path.abspath("static/")

@app.route("/")
def showIndex():
    return render_template("example.html")

@app.route("/static/<path:path>")
def staticRequest(path):
    print(path)
    return send_from_directory('static',path)
app.run()





