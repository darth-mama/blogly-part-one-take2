"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


with app.app_context():
    connect_db(app)
    db.create_all()

app.app_context().push()


@app.route('/')
def root():
    """Redirects to list of users"""
    return redirect("/users")


@app.route("/users")
def users_index():
    """Show all users"""
    """Make thse links to view the detail page for the user"""
    """Have a link here to the add-user form"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)


@app.route("/users/new", methods=['GET', 'POST'])
def create_user():
    """Shows an add form for users"""
    """Pocess the add form, adding a new user and going back to /users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/{new_user.id}")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("/users/details.html", user=user)
