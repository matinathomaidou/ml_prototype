#!/usr/bin/python3.5
#-*-coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user, current_user
from flask import redirect
from flask import url_for
from flask import request
from flask_login import logout_user
from forms import RegistrationForm
from forms import LoginForm
from forms import AdminUserCreateForm
from forms import AdminUserPW
import config
from functools import wraps
from flask import current_app

def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))
        
        return fn(*args, **kwargs)
            
    return decorated_view


if config.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper
    
from user import User
from passwordhelper import PasswordHelper

DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
app.secret_key = config.secret_key

login_manager = LoginManager(app)



def is_admin():
     try:   
        curr = current_user.get_id()
        user = DB.get_user(curr)
        if user['admin'] == 'Y':
            return True
        else:
            return False
     except:
        return True
        

@app.route("/")
@ssl_required
def home():
    if config.reg_open:
        return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())
    else:
        return render_template("home.html", loginform=LoginForm(), registrationform=None)

    
@app.route("/login", methods=["POST"])
@ssl_required
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password((form.loginpassword.data).encode(), stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
        form.loginemail.errors.append("Email or password invalid")
    if config.reg_open:
       return render_template("home.html", loginform=form, registrationform=RegistrationForm())
    else:
       return render_template("home.html", loginform=form, registrationform=None)
  

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))       
    
@app.route("/register", methods=["POST"])
@ssl_required
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('home.html', loginform=LoginForm, registrationform=form)
        salt = PH.get_salt()
        hashed = PH.get_hash((form.password2.data).encode() + salt)
        is_admin = 'N'
        DB.add_user(form.email.data, salt, hashed, is_admin)
        return render_template("home.html", loginform=LoginForm(), registrationform=form, onloadmessage="Registration successful. Please log in to continue.  Thank you!.")
    return render_template("home.html", loginform=LoginForm(), registrationform=form)

    
@app.route("/dashboard")
@ssl_required
@login_required
def dashboard():
    return render_template("dashboard.html")
    
@app.route("/admin/web_log")
@login_required
@ssl_required
def web_log():
    if (is_admin()):
        return render_template('logs.html')
    else:
        return redirect(url_for('dashboard'))  

@app.route("/admin/access_log")
@login_required
@ssl_required
def access_log():
    if (is_admin()):
        return render_template('auth_logs.html')
    else:
        return redirect(url_for('dashboard'))  

@app.route("/admin/ftp_log")
@login_required
@ssl_required
def ftp_log():
    if (is_admin()):
        return render_template('ftp_logs.html')
    else:
        return redirect(url_for('dashboard'))  



@app.route("/account")
@login_required
@ssl_required
def account():
    return render_template("account.html")
    
    
@app.route('/admin')
@login_required
@ssl_required
#@admin_login_required
def home_admin():  
    if (is_admin()):
        return render_template('admin-home.html')
    else:
        return redirect(url_for('dashboard'))


@app.route('/admin/users-list')
@login_required
@ssl_required
#@User.is_admin()
def users_list_admin():
    if (is_admin()):
        users = DB.list_user()
        return render_template('users-list-admin.html', users=users)
    else:
        return redirect(url_for('dashboard'))
   
@app.route('/admin/users-list/delete-user/<id>', methods=["GET","POST"])
@login_required
@ssl_required
#@User.is_admin()
def users_delete_admin(id):
    if (is_admin()):
        DB.del_user(id)
        return redirect(url_for('users_list_admin'))
    
    else:
        return redirect(url_for('dashboard'))
    
@app.route("/admin/registered", methods=["POST"])
@login_required
@ssl_required
#@User.is_admin()
def register_admin():
    if (is_admin()):
        form = AdminUserCreateForm(request.form)
        if form.validate():
            if DB.get_user(form.email.data):
                form.email.errors.append("Email address already registered")
                return render_template("admin_register.html", loginform=None, registrationform=form)
            salt = PH.get_salt()
            hashed = PH.get_hash((form.password2.data).encode() + salt)
            isadmin = 'N'
            DB.add_user(form.email.data, salt, hashed, isadmin)
            users = DB.list_user()
            return render_template("users-list-admin.html", users=users, onloadmessage="User Registration successful. Please inform the user.  Thank you!.")
        else:
            if DB.get_user(form.email.data):
                form.email.errors.append("Email address already registered")   
            form.email.errors.append("Fix errors and re-submit!")    
            return render_template("admin_register.html", loginform=None, registrationform=form) 
    
    else:
        return redirect(url_for('dashboard'))

  
@app.route("/admin/requested_reg")
@login_required
@ssl_required
#@User.is_admin()
def admin_add():
    if (is_admin()):  
        return render_template("admin_register.html", loginform=None, registrationform=AdminUserCreateForm())
       
    else:
        return redirect(url_for('dashboard'))
 
@app.route("/admin/pw_reset")
@login_required
@ssl_required
#@User.is_admin()
def admin_reset():
    if (is_admin()):  
       return render_template("admin_password.html", loginform=None, registrationform=AdminUserPW())
       
    else:
        return redirect(url_for('dashboard'))
       

@app.route("/admin/pw_submit", methods=["POST"])
@login_required
@ssl_required
#@User.is_admin()
def admin_pw_update():    
    if (is_admin()):  
        form = AdminUserPW(request.form)
        if form.validate():
            if DB.get_user(form.email.data):
                salt = PH.get_salt()
                hashed = PH.get_hash((form.password2.data).encode() + salt)
                isadmin = 'N'
                DB.pw_user_update(form.email.data, salt, hashed, isadmin)
                users = DB.list_user()
                return render_template("users-list-admin.html", users=users, onloadmessage="Password changed - Inform the user.  Thank you!.")
            else:
                form.email.errors.append("error! email not known!")
                return render_template("admin_password.html", loginform=None, registrationform=form)    
        else:
                form.email.errors.append("Fix errors and re-submit!")
                return render_template("admin_password.html", loginform=None, registrationform=form)   
    else:
        return redirect(url_for('dashboard'))
  

if __name__ == "__main__":
    context = ('host.crt', 'host.key')
    app.run(host='0.0.0.0', port=80, ssl_context=context, threaded=True, debug=True)   
    

