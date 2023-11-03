import json
import os
from datetime import datetime

from flask import Flask, flash, logging, redirect, render_template, request, session, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment

from app import create_app, db
from app.main.forms import LoginForm, SignupForm
from app.models import Event, EventInterest, Interest, Organizer, OrganizerInterest, User

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Interest=Interest,
        OrganizerInterest=OrganizerInterest,
        Organizer=Organizer,
        EventInterest=EventInterest,
        Event=Event,
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('myAccount')

        flash("Invalid email or password")

    return render_template('login.html', form=form)

@app.route("/myAccount", methods=["GET", "POST"])
@login_required
def myAccount():
    return render_template("myAccount.html", name=current_user.name)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        hashed_password = generate_password_hash(form.password.data)
        if user is None and email is None:
            if "utoronto" in form.email.data.split("@")[1]:
                user = User(name=form.name.data, email=form.email.data, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                session["name"] = form.name.data
                session["email"] = form.email.data
                session["faculty"] = form.faculty.data
                session["major"] = form.major.data
                session["campus"] = form.campus.data
                session["yearOfStudy"] = form.year_of_study.data
                return redirect(url_for("users.user_list"))
            else:
                flash("You may only register with your UofT email")
        else:
            flash("Account with this name/email address already exists!")

    return render_template("index.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return render_template("user/detail.html", user=user)


# @app.route("/organizer/create", methods=["POST"])
# def organizer_create():
#      organizer = Organizer(
#          organizer_name=request.form["organizer_name"],
#          organizer_email=request.form["organizer_email"],
#          description=request.form["description"],
#          contact_email=request.form["contact_email"],
#          website=request.form["website"],
#          instagram=request.form["instagram"],
#          linkedin=request.form["linkedin"],
#          campus=request.form["campus"],
#      )
#      db.session.add(organizer)
#      db.session.commit()
#      return render_template("organizer/create.html")


# @app.route("/organizer/<int:id>", methods=["GET"])
# def get_organizer(id):
#     pass


# @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
# def user_delete(id):
# 	user = db.get_or_404(User, id)
#     if request.method == "POST":
#         db.session.delete(user)
#         db.session.commit()
#         return redirect(url_for("user_list"))
#     return render_template("user/delete.html", user=user)

if __name__ == "__main__":
    app.run()
