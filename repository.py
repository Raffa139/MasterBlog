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


def get_blog_post_by_id(id):
    posts = get_blog_posts()

    try:
        post_by_id, = [post for post in posts if post["id"] == id]
        return post_by_id
    except ValueError:
        return None


def add_blog_post(author, title, content):
    if any([not author, not title, not content]):
        raise ValueError("Author, Title, and Content needed to create blog post")

    blog_posts = get_blog_posts()
    id = next_id(posts=blog_posts)

    blog_posts.append({
        "id": id,
        "author": author,
        "title": title,
        "content": content,
        "likes": 0
    })

    serialize_blog_posts(blog_posts)


def update_blog_post(id, author, title, content):
    if any([not author, not title, not content]):
        raise ValueError("Author, Title, and Content needed to update blog post")

    blog_posts = get_blog_posts()
    post = get_blog_post_by_id(id)

    if not post:
        raise KeyError()

    blog_posts.remove(post)

    blog_posts.append({
        "id": id,
        "author": author,
        "title": title,
        "content": content,
        "likes": post["likes"]
    })

    serialize_blog_posts(blog_posts)


def delete_blog_post(id):
    if not id:
        raise ValueError("No id provided")

    posts_to_keep = [post for post in get_blog_posts() if post["id"] != id]
    serialize_blog_posts(posts_to_keep)


def increment_likes(id):
    if not id:
        raise ValueError("No id provided")

    blog_posts = get_blog_posts()
    post = get_blog_post_by_id(id)

    if not post:
        raise KeyError()

    blog_posts.remove(post)

    blog_posts.append({
        "id": id,
        "author": post["author"],
        "title": post["title"],
        "content": post["content"],
        "likes": post["likes"] + 1
    })

    serialize_blog_posts(blog_posts)


def next_id(*, posts):
    used_ids = [post["id"] for post in posts]
    id = len(posts)

    while id in used_ids:
        id += 1

    return id
