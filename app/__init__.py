from flask import Flask, flash
from flask import render_template, request, redirect, url_for
from flask_seasurf import SeaSurf
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db
from app.system import *
from app.validate import *


def create_app():
    app = Flask(__name__)
    app.secret_key = "hopper_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///config.db"

    # csrf protection
    SeaSurf(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    db.init_app(app)

    from app.models import UserModel

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    @app.route('/')
    def dashboard_page():
        cards = []

        load = get_average_load_5()
        cards.append({
            "title": "Average Load (5 min)",
            "percent": load,
        })

        memory = get_memory_usage()
        cards.append({
            "title": "Memory Usage",
            "percent": memory,
        })

        for disk in get_disks_usage():
            cards.append({
                "title": f"Disk Usage ({disk.get('mount')})",
                "percent": disk.get('usage')
            })

        boot_time = get_boot_time()
        cards.append({
            "title": "Time Elapsed Since Boot",
            "text": boot_time,
        })

        number_of_users = get_number_of_users()
        cards.append({
            "title": "Number of Users",
            "text": number_of_users,
        })

        return render_template('dashboard.html', cards=cards)

    @app.route('/user')
    def user_page():
        return render_template('user.html', users=get_user())

    @app.route('/proc')
    def process_page():
        return render_template('proc.html', process=get_process(only_user=get_usernames()))

    @app.route("/login", methods=["POST"])
    def login():
        source_url = request.referrer

        if current_user.is_authenticated:
            flash("You're already logged in", "warning")
            return redirect(source_url)

        email = request.form.get("email")

        if not validate_email(email):
            flash("Invalid email address", "error-auth")
            return redirect(request.referrer)

        user = UserModel.query.filter_by(
            email=email).first()

        if user is not None and check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            flash("You've successfully logged in", "success")
        else:
            flash("Authentication failed, check your username and password", "error-auth")

        return redirect(source_url)

    @app.route('/register', methods=["POST"])
    def register():
        email = request.form.get("email")

        if not validate_email(email):
            flash("Invalid email address", "error-auth")
            return redirect(request.referrer)

        if UserModel.query.filter_by(email=email).first() is not None:
            flash("This email is already registered", "error-auth")
            return redirect(request.referrer)

        username = request.form.get("username")

        if not validate_username(username):
            flash("Invalid username", "error-auth")
            return redirect(request.referrer)

        password = generate_password_hash(request.form.get("password"))

        user = UserModel(email=email, username=username, password=password)
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        flash("You've successfully registered an account", "success")
        return redirect(request.referrer)

    @app.route("/logout")
    def logout():
        logout_user()
        flash("You've been successfully logged out", "success")
        return redirect(request.referrer)

    return app
