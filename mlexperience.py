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
from forms import UserPW
from forms import UserPref
import config
from functools import wraps
from flask import current_app
from weather import get_local_time, query_api


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

sec_files = config.sec_files

if config.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper
    
from user import User
from passwordhelper import PasswordHelper

DB = DBHelper()
PH = PasswordHelper()


def is_admin():
     try:   
        curr = current_user.get_id()
        user = DB.get_user(curr)
        if user['admin'] == 'Y':
            return True
        else:
            return False
     except:
        return False
    
 
class SecuredStaticFlask(Flask):
    def send_static_file(self, filename):
        if (filename.strip() in sec_files):
            if is_admin():
                return super(SecuredStaticFlask, self).send_static_file(filename)
            else:
                try:
                    if(current_user.is_authenicated()):
                        return render_template("dashboard.html")
                except:
                    if config.reg_open:
                        return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())
                    else:
                        return render_template("home.html", loginform=LoginForm(), registrationform=None)  
        else:
            return super(SecuredStaticFlask, self).send_static_file(filename)     
        
    def send_file(self, filename):
        print(filename)
        sec_files = ['log.txt', 'ftp_log.txt','auth_log.txt']
        if (filename.strip() in sec_files):
            if is_admin():
                return super(SecuredStaticFlask, self).send_file(filename)
            else:
                try:
                    if(current_user.is_authenicated()):
                        return render_template("dashboard.html")
                except:
                    if config.reg_open:
                        return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())
                    else:
                        return render_template("home.html", loginform=LoginForm(), registrationform=None) 
        else:
            return super(SecuredStaticFlask, self).send_file(filename)          
        
    def send_from_directory(self, filename):
        print(filename)
        sec_files = ['log.txt', 'ftp_log.txt','auth_log.txt']
        if (filename.strip() in sec_files):
            if is_admin():
                return super(SecuredStaticFlask, self).send_from_directory(filename)
            else:
                try:
                    if(current_user.is_authenicated()):
                        return render_template("dashboard.html")
                except:
                    if config.reg_open:
                        return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())
                    else:
                        return render_template("home.html", loginform=LoginForm(), registrationform=None) 
        else:
            return super(SecuredStaticFlask, self).send_from_directory(filename)     

    def get_send_file_max_age(self, filename):
            return 0

        
       
app = SecuredStaticFlask(__name__)
app.secret_key = config.secret_key

login_manager = LoginManager(app)

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
    
    
@app.route("/dashboard/news_service")
@ssl_required
@login_required
def news_service():
    return render_template("model.html")    
    
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

@app.route("/account", methods=['GET'])
@login_required
@ssl_required
def account():
    curr = current_user.get_id()
    profile = DB.user_profile_read(curr)  

    return render_template("account.html", passwordform=UserPW(), toggle = True, userpref=UserPref(), profile=profile, mode='')
    
    
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

   
@app.route('/admin/users-list/edit-user/<id>', methods=["GET","POST"])
@login_required
@ssl_required
#@User.is_admin()
def users_edit_admin(id):
    if (is_admin()):
        DB.toggle_admin(id)
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


@app.route('/dashboard/news_service/city/', methods=['POST'])
def index():
    data = []
    error = None
    if request.method == 'POST':
        city1 = request.form.get('city1')
        city2 = request.form.get('city2')
        for c in (city1, city2):
            resp = query_api(c)
            if resp:
                data.append(resp)
        if len(data) != 2:
            error = 'Did not get complete response from Weather API'
    return render_template("model.html",
                           data=data,
                           error=error,
                           time=get_local_time)

@app.route("/user/pw_submit", methods=["POST"])
@login_required
@ssl_required
#@User.is_admin()
def user_pw_update():    
        form = UserPW(request.form)
        curr = current_user.get_id()
        if form.validate():
                salt = PH.get_salt()
                hashed = PH.get_hash((form.password2.data).encode() + salt)
                DB.pw_user_update(curr, salt, hashed, 'N')
                return render_template("account.html", onloadmessage="Password changed - Inform the user.  Thank you!.", passwordform=UserPW(), userpref=UserPref())

        else:
                form.password.errors.append("Fix errors and re-submit!")               
                return render_template("account.html", onloadmessage="Password error", passwordform=form, userpref=None, toggle= False)   
                
@app.route("/user/profile_submit", methods=["POST"])
@login_required
@ssl_required
def user_profile_update(mode):
    print(mode)
    form = UserPref(request.form)
    curr = current_user.get_id()
    profile = {}
    profile['name'] = form.name.data
    profile['city'] = form.city.data
    profile['news'] = form.news_pref.data
    profile['currency'] = form.currency.data
    profile['share'] = form.share.data
    if form.validate():
        DB.user_profile_update(curr, profile)       
        return redirect(url_for('account'))    
    
    else:
        form.name.errors.append('Fix errors')
        return render_template("account.html", passwordform=None, userpref=form, toggle= True, profile=profile, mode='') 


                
  

if __name__ == "__main__":
    context = ('host.crt', 'host.key')
    app.run(port=80, ssl_context=context, threaded=True, debug=True)   
    


