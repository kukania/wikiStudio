from flask import Blueprint,request,session
from .databaseClass import DatabaseConnector

connector=DatabaseConnector()

loginTask=Blueprint('loginTask',__name__,template_folder='templates');

@loginTask.route('/login',methods=["POST"])
def login():
    query="select * from user where UID='"+request.form.get("ID")+"' and pwd=md5('"+request.form.get("pwd")+"')";
    res=connector.query_select(query)
    if res['NUM']==1:
        session['UID']=res['ROW'][0]['ID']
        session['nickname']=res['ROW'][0]['nickname']
        query="select entry.CONTENTID,TITLE from entry join content on entry.CONTENTID=content.CONTENTID where entry.ID="+str(session['UID']);
        session['treeNav']=connector.query_select(query);
        print(session['treeNav']);
        return "<script>alert('success'); location.href='./';</script>"
    else:
        return "<script>alert('No user is here'); location.href='./'</script>"


@loginTask.route('/enrollment',methods=["POST"])
def enrollment():
    query="insert into user (pwd,UID,nickname) values (md5('"+request.form.get("pwd")+"'),'"+request.form.get("ID")\
          +"','"+request.form.get("nickname")+"')"
    num=connector.query_insert(query)
    if num==1:
        #session setting
        res=connector.query_select("select ID from user where UID='" + request.form.get("ID") + "'");
        session['UID']=res['ROW']['ID']
        session['nickname']=request.form.get('nickname')
        query = "insert into content (DEPTH,ID,ISCODE,ISPAGE,CONTENTS,TITLE) values (0,"+str(session['UID'])+",0,1,'index','mainpage')"
        connector.query_insert(query)
    else:
        return "error"
    return "<script> alert('complete');location.href='./'</script>"

@loginTask.route('/logout')
def logout():
    session.clear()
    return "<script>location.href='./';</script>"