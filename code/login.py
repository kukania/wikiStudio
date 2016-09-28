from flask import Blueprint,request,session
from .databaseClass import DatabaseConnector

connector=DatabaseConnector()

loginTask=Blueprint('loginTask',__name__,template_folder='templates');

@loginTask.route('/login',methods=["POST"])
def login():
    query="select * from user where UID='"+request.form.get("ID")+"' and pwd=md5('"+request.form.get("pwd")+"')";
    res=connector.query_select(query)
    if res['NUM']==1:
        session['UID']=res['ROW']['ID']
        session['nickname']=res['ROW']['nickname']
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
        session['UID']=connector.query_select("select ID from user where UID='"+request.form.get("ID")+"'");
        session['nickname']=request.form.get("nickname");
    else:
        return "error"
    return "<script> alert('complete');location.href='./'</script>"