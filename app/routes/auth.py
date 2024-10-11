from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..models.user import Role
from ..services.auth_service import login_user_service, register_user_service
from ..forms.auth.signup_form import SignupForm  # Adjust the import as necessary
from ..services.auth_service import create_user  # Example service to handle user creation
from ..forms.auth.login_form import LoginForm  # Adjust import as necessary
from flask_login import login_user
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = login_user_service(form.username.data, form.password.data)
        if user:
            print(f"User {user.username} found, logging in")  # Debugging
            login_user(user)
            flash('Logged in successfully!', 'success')
            # Check if the user is an admin
            if user.role == Role.ADMIN:  # Adjust according to your role implementation
                return render_template('admin/index.html',user=user)  # Redirect to admin index page
            else:
                return redirect(url_for('blog.list_blogs'))  # Redirect to user blogs
        else:
            flash('Invalid username or password.', 'danger')
            print("Login failed")  # Debugging
    else:
        print("Form validation failed")  # Debugging
    return render_template('auth/login.html', form=form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Call your service to create the user
        if create_user(username, email, password):  # Implement the user creation logic
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))  # Redirect to login or another page
        else:
            flash('Error creating account. Please try again.', 'danger')
    return render_template('auth/signup.html', form=form)