from flask import Blueprint,request

loginTask=Blueprint('loginTask',__name__,template_folder='templates');

@loginTask.route('/login',method=["POST"])
def login():
    return request.forms.get("")
