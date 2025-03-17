import json

REPOSITORY_FILE = "data/blog-posts.json"


def get_blog_posts():
    with open(REPOSITORY_FILE, encoding="utf-8") as file:
        return json.load(file)


def add_blog_post(author, title, content):
    pass


def update_blog_post(id, author, title, content):
    pass


def delete_blog_post(id):
    pass
