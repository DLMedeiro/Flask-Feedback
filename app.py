# Questions:
    # When account is logged out, users can no access profiles.  When a user is logged in, they have access to other users profiles if user/"username" is updated in the browser

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User_Info, Feedback
from forms import CreateUserForm, LoginForm, CreateFeedback
import os
import re


app = Flask(__name__)

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','secret' )
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def index():
    """GET / - Redirect to /register."""

    return redirect ("/register")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    """GET /register - Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name. Make sure you are using WTForms and that your password input hides the characters that the user is typing!"""

    form = CreateUserForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            user = User_Info.register(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
            db.session.add(user)
            db.session.commit()

            session['user_username'] = user.username
            return redirect("/feedback")
        except:
            flash(f'The username "{username}" is already in use, please choose another username')
            return render_template("register.html", form = form)
    else:
        return render_template("register.html", form = form)

@app.route('/feedback')
def feedback():
    feedback = Feedback.query.all()
    return render_template('feedback.html', feedback = feedback)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User_Info.authenticate(username = username, password = password)
        if user:
            session['user_username'] = user.username
            return redirect('/feedback')
            # return redirect("/user/" + session['user_username'])
        else:
            return render_template('login.html', form = form)

    return render_template('login.html', form = form)

@app.route('/user/<active>')
def secret(active):

    if 'user_username' not in session:
        return redirect('/login')

    active_user =  User_Info.query.get_or_404(active)

    if active_user.username == session['user_username']:
        feedback = Feedback.query.all()
        return render_template('userpage.html', active_user= active_user, feedback = feedback)
    else:
        flash("You must be logged in to view this page")
        return redirect('/login')


@app.route('/user/<active>/delete')
def delete_user(active):
    # Will prevent from going straight to user/username if not logged in.  Will not prevent user/*anyusername if already logged in
    if "user_username" not in session:
        return redirect('/login')
    else:
        session.pop('user_username')
        active_user =  User_Info.query.get_or_404(active)
        feedback = Feedback.query.filter_by(username_id = active).delete()

        # db.session.delete(feedback)
        db.session.commit()

        db.session.delete(active_user)
        db.session.commit()

        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user_username')
    return redirect('/login')


@app.route('/user/<active>/feedback/add', methods = ['GET', 'POST'])
def addFeedback(active):
    """Active = username"""

    if 'user_username' not in session:
        return redirect('/login')

    active_user =  User_Info.query.get_or_404(active)
    form = CreateFeedback()

    if active_user.username == session['user_username']:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            username_id = active_user.username

            feedback = Feedback(title = title, content = content, username_id = session['user_username'])
            db.session.add(feedback)
            db.session.commit()

            return redirect("/user/" + str(username_id))
        else:
            return render_template('createFeedback.html', form = form)
    else:
        flash("You must be logged in to view this page")
        return redirect('/login')


@app.route('/feedback/<feedback_id>/edit')
def editFeedback_page(feedback_id):
    if "user_username" not in session:
        return redirect('/login')
    feedback_item =  Feedback.query.get_or_404(feedback_id)

    return render_template('editFeedback.html', feedback_item = feedback_item)
@app.route('/feedback/<feedback_id>/edit', methods = ['POST'])

def editFeedback(feedback_id):
    if "user_username" not in session:
        return redirect('/login')


    title = request.form['title']
    content = request.form['content']

    feedback = Feedback.query.get(feedback_id)
    username = feedback.username_id
    feedback.edit_feedback(title, content, username)

    db.session.add(feedback)
    db.session.commit()

    return redirect("/user/" + str(username))

@app.route('/feedback/<feedback_id>/delete')
def deleteFeedback(feedback_id):
    if "user_username" not in session:
        return redirect('/login')

    feedback_item =  Feedback.query.get_or_404(feedback_id)

    username = feedback_item.username_id
    
    db.session.delete(feedback_item)
    db.session.commit()

    return redirect("/user/" + str(username))