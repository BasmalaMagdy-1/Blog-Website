from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.user import User
from app.models.blog import Blog

from app.db import db

admin_bp = Blueprint('admin', __name__)
from flask import abort
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function
@admin_bp.route('/users', methods=['GET'])
def manage_users():
    users = User.query.all()  # Get all users
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/', methods=['GET'])
def index():
    return render_template('admin/index.html', user=current_user)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found.', 'danger')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/blogs', methods=['GET'])
@admin_required  # Ensure only admins can access this route
def manage_blogs():
    blogs = Blog.query.all()  # Fetch all blogs from the database
    return render_template('admin/manage_blogs.html', blogs=blogs)

@admin_bp.route('/blog/<int:blog_id>/delete', methods=['POST'])
@admin_required  # Ensure only admins can access this route
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog:
        db.session.delete(blog)
        db.session.commit()
        flash('Blog deleted successfully!', 'success')
    else:
        flash('Blog not found.', 'danger')
    return redirect(url_for('admin.manage_blogs'))