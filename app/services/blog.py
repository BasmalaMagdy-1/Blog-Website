from ..models.blog import Blog
from app.db import db
from flask_login import current_user
def get_all_blogs():
    return Blog.query.all()

def create_blog_service(title, content):
    new_blog = Blog(title=title, content=content, author_id=current_user.id)
    db.session.add(new_blog)
    db.session.commit()
    return True

def get_blog_by_id(blog_id):
    return Blog.query.get(blog_id)

def update_blog_service(blog_id, title, content):
    blog = get_blog_by_id(blog_id)
    if blog:
        blog.title = title
        blog.content = content
        db.session.commit()
        return True
    return False

def delete_blog_service(blog_id):
    blog = get_blog_by_id(blog_id)
    if blog:
        db.session.delete(blog)
        db.session.commit()
        return True
    return False
