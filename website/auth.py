from flask import Flask , Blueprint ,render_template,request,flash,redirect,url_for
from .modules import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method =="POST":
        user_email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = user_email).first()
        if user is None:
            flash("Account doesn\'t exist , please register" ,category='error')
        else:
            if check_password_hash(user.password ,password):
                flash ("Logged in successfully")
                login_user(user)
                return redirect (url_for('views.home'))
            else:
                flash("Incorrect password. Please try again.", category='error')
    return render_template('login.html', user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect (url_for('auth.login'))



@auth.route('/sign-up',methods=["GET","POST"])
def sign_up():
    if request.method =='POST':
        user_email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        user = User.query.filter_by(email = user_email).first()
        if user:
            flash("Email already exists." ,category='error')
        elif password != confirm_password:
            flash("Passwords don\'t match" , category='error')
        else:
            new_user = User(
                email = user_email, 
                first_name = first_name ,
                last_name = last_name,
                password = generate_password_hash(password,method='pbkdf2:sha256')
                )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully', category='success')
            login_user(new_user)
            return redirect (url_for('views.home'))  
    
    return render_template('signup.html',user=current_user)


