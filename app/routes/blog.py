from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..db import db
from ..services.blog import get_all_blogs, create_blog_service, get_blog_by_id, update_blog_service, delete_blog_service
from ..forms.blogs.create_form import CreateForm  # Adjust this import as necessary
from app.models.blog import Blog  # Make sure to import the Blog model
from flask_login import current_user

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/list', methods=['GET'])
def list_blogs():
    blogs = get_all_blogs()
    return render_template('blog/list.html', blogs=blogs)

@blog_bp.route('/view/<int:id>', methods=['GET'])
def view(id):
    blog = get_blog_by_id(id)  # Get a single blog object
    if blog is None:
        flash('Blog not found.', 'danger')  # Handle the case where the blog does not exist
        return redirect(url_for('blog.list_blogs'))
    return render_template('blog/view.html', blog=blog)

@blog_bp.route('/like/<int:blog_id>', methods=['POST'])
def like(blog_id):
    blog = get_blog_by_id(blog_id)
    if blog:
        blog.likes += 1
        db.session.commit()  # Commit the changes to the database
        flash('You liked the blog!', 'success')
    else:
        flash('Blog not found.', 'danger')
    return redirect(url_for('blog.view', id=blog_id))

@blog_bp.route('/dislike/<int:blog_id>', methods=['POST'])
def dislike(blog_id):
    blog = get_blog_by_id(blog_id)
    if blog:
        blog.dislikes += 1
        db.session.commit()  # Commit the changes to the database
        flash('You disliked the blog!', 'success')
    else:
        flash('Blog not found.', 'danger')
    return redirect(url_for('blog.view', id=blog_id))

@blog_bp.route('/create', methods=['GET', 'POST'])
def create_blog():
    form = CreateForm()  # Create an instance of your form
    if request.method == 'POST':
        if form.validate_on_submit():  # Validate the form input
            title = form.title.data
            content = form.content.data
            if create_blog_service(title, content):
                flash('Blog created successfully!', 'success')
                return redirect(url_for('blog.list_blogs'))
            else:
                flash('Error creating blog.', 'danger')
    return render_template('blog/create.html', form=form)


@blog_bp.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit(blog_id):
    blog = get_blog_by_id(blog_id)
    if blog is None:
        flash('Blog not found.', 'danger')
        return redirect(url_for('blog.list_blogs'))

    form = CreateForm(obj=blog)  # Pass the blog object to pre-fill the form
    if request.method == 'POST':
        if form.validate_on_submit():  # Validate the form input
            # Call the update service with the blog ID and new data
            if update_blog_service(blog_id, form.title.data, form.content.data):
                flash('Blog updated successfully!', 'success')
                return redirect(url_for('blog.view', id=blog.id))
            else:
                flash('Error updating blog.', 'danger')

    return render_template('blog/edit.html', form=form, blog=blog)