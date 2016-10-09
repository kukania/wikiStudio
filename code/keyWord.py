from flask import Blueprint,request,session,render_template
from .databaseClass import DatabaseConnector
import mistune

makeContents=Blueprint('keyword',__name__,template_folder='templates')
markDown=mistune()
connector=DatabaseConnector()

@makeContents.route('read/<user_id>/<article_id>')
def contentsParser(user_id,article_id):
    query="select * from content where ID="+user_id+" and CONTENTID="+article_id
    res=connector.query_select(query)
    if res['NUM']==0:
        return render_template("example.html",content="not found")
    else:
        return render_template("example.html",contents=markDown(res["ROW"]))
