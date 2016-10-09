from flask import Blueprint,request,session,render_template
from .databaseClass import DatabaseConnector
import re
connector=DatabaseConnector()
insert=Blueprint('insert',__name__,template_folder='templates')

@insert.route('/insert')
def insertIdx():
    if 'nickname' in session:
        return render_template("insert_template.html",session=session,nickname=session['nickname'])
    else:
        return render_template("not_Found.html")

@insert.route('/insert/<content_id>')
def insertContentId(content_id):
    query="select * from content where CONTENTID="+content_id+" and ID="+str(session['UID'])
    res=connector.query_select(query)
    if res["NUM"]==0:
        return render_template("not_Found.html")
    else:
        return render_template("insert_template.html",session=session,nickname=session['nickname'],content=res['ROW'][0]['CONTENTS'],target=content_id)


def branchInsert(content,title,content_id,session):
    query = "update content set CONTENTS=" + content + ", TITLE=" + title + " where CONTENTID=" + content_id + " and ID=" + str(session['UID'])
    connector.query_select(query)
    return

@insert.route('/submit/<contnet_id>',methods=['POST'])
def submit(content_id):
    query = "select * from content where CONTENTID=" + content_id + " and ID=" + str(session['UID'])
    res=connector.query_select(query)
    if res['ROW'][0]['ISPAGE'] == 0:
        title=re.search("(===)(\w+\w|\w)*(===)",request.form.get('content')).group()
        branchInsert(request.form.get('content'),title,content_id,session)
    else:
        contentAll=request.get.form('content')
        title = request.get.form('title')
        resSearch=re.search("(===)(\w+\w|\w)*(===)",contentAll)

        if resSearch is None:
            content = contentAll[0:len(contentAll)]
            branchInsert(content, title, content_id, session)
            return
        else:
            content=contentAll[0:resSearch.span()[0]]

        branchInsert(content,title,content_id,session)

        while True:
            tempIdx=resSearch.span()[1]+1;
            title=contentAll[resSearch.span()[0]:resSearch.span()[1]]
            resSearch = re.search("(===)(\w+\w|\w)*(===)", contentAll[resSearch.span()[1]:len(contentAll)-1])

            if resSearch is None:
                content = contentAll[tempIdx:len(contentAll)]
                branchInsert(content, title, content_id, session)
                break;
            else:
                content = contentAll[0:resSearch.span()[0]]
            branchInsert(content, title, content_id, session)
    return
