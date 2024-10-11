from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..services.user import get_user_profile,update_user_profile_service,get_all_users
from flask_login import current_user
user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Handle profile update
        username = request.form.get('username')
        email = request.form.get('email')
        if update_user_profile_service(username, email):
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Error updating profile.', 'danger')

    user = get_user_profile()  # Get the current user's profile

    # Check if the user is admin and redirect to the admin page
    if current_user.is_authenticated and current_user.is_admin():
        return render_template('admin/index.html', user=user)

    # If not admin, render the regular profile page
    return render_template('user/profile.html', user=user)

@user_bp.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()  # List all users (if applicable)
    return render_template('admin/manage_users.html', users=users)
