import json

REPOSITORY_FILE = "data/blog-posts.json"


def serialize_blog_posts(posts):
    with open(REPOSITORY_FILE, mode="w", encoding="utf-8") as file:
        json.dump(posts, file)


def deserialize_blog_posts():
    with open(REPOSITORY_FILE, encoding="utf-8") as file:
        return json.load(file)


def get_blog_posts():
    return deserialize_blog_posts()


def add_blog_post(author, title, content):
    if any([not author, not title, not content]):
        raise ValueError("Author, Title, and Content needed to create blog post")

    blog_posts = get_blog_posts()
    id = next_id(posts=blog_posts)

    blog_posts.append({
        "id": id,
        "author": author,
        "title": title,
        "content": content
    })

    serialize_blog_posts(blog_posts)


def update_blog_post(id, author, title, content):
    pass


def delete_blog_post(id):
    pass


def next_id(*, posts):
    used_ids = [post["id"] for post in posts]
    id = len(posts)

    while id in used_ids:
        id += 1

    return id
