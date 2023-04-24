from flask import Flask, render_template, redirect, request, flash, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from data import db_session
from data.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin
import courses_api
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'andrew-bakradze'
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index2.html', title=str(current_user.get_name()))
    else:
        return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == request.form['email']).first()
        print(user)
        if user and check_password_hash(user.hashed_password, request.form['password']):
            userLogin = UserLogin().create(user)
            login_user(userLogin, remember=True)
            return redirect(url_for('index'))
    return render_template('index3.html')


@app.route('/register', methods=["POST", "GET"])

def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['password']) > 4:
            hash = generate_password_hash(request.form['password'])
            user = User()
            user.name = request.form['name']
            user.hashed_password = hash
            user.courses = 'none'
            user.email = request.form['email']
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            print('123')
            return redirect(url_for('index'))
    return render_template('index4.html')


@login_required


@app.route('/profile', methods=["POST", "GET"])
def profile():
    data = requests.get(f"http://localhost:8000/api/courses/{current_user.get_id()}").json()
    print(data)
    if request.method == 'POST':
        logout_user()
        return redirect("/")
    return render_template('profile.html', title=str(current_user.get_name()), courses=data)



@login_required

@app.route('/courses')
def courses():
    return render_template('courses.html')


@login_required

@app.route('/flask_base', methods=["POST", "GET"])
def flask_base():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        db_sess.query(User).filter(User.id == current_user.get_id()).update({"courses": f"{current_user.get_courses()}, flask_base"}, synchronize_session='fetch')
        db_sess.commit()
    return render_template('flask_base.html')


@app.route('/about')
def about():
    return render_template('about.html')



def main():
    db_session.global_init("db/subScript.db")
    app.register_blueprint(courses_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()