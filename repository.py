import json

REPOSITORY_FILE = "data/blog-posts.json"


def serialize_blog_posts(posts):
    """
    Serializes a list of blog posts to a JSON file.

    Args:
        posts (list[dict]): A list of dictionaries representing blog posts.
    """
    with open(REPOSITORY_FILE, mode="w", encoding="utf-8") as file:
        json.dump(posts, file)


def deserialize_blog_posts():
    """
    Deserializes a list of blog posts from a JSON file.

    Returns:
        list[dict]: A list of dictionaries representing blog posts.
    """
    with open(REPOSITORY_FILE, encoding="utf-8") as file:
        return json.load(file)


def get_blog_posts():
    """
    Retrieves all blog posts from the repository.

    Returns:
        list[dict]: A list of dictionaries representing blog posts.
    """
    return deserialize_blog_posts()


def get_blog_post_by_id(id):
    """
    Retrieves a blog post by its ID.

    Args:
        id (int): The ID of the blog post.

    Returns:
        dict or None: A dictionary representing the blog post, or None if not found.
    """
    posts = get_blog_posts()

    try:
        post_by_id, = [post for post in posts if post["id"] == id]
        return post_by_id
    except ValueError:
        return None


def add_blog_post(author, title, content):
    """
    Adds a new blog post to the repository.

    Args:
        author (str): The author of the blog post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.

    Raises:
        ValueError: If any of the required arguments are missing.
    """
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
    """
    Updates an existing blog post in the repository.

    Args:
        id (int): The ID of the blog post to update.
        author (str): The updated author of the blog post.
        title (str): The updated title of the blog post.
        content (str): The updated content of the blog post.

    Raises:
        ValueError: If any of the required arguments are missing.
        KeyError: If the blog post with the given ID is not found.
    """
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
    """
    Deletes a blog post from the repository.

    Args:
        id (int): The ID of the blog post to delete.

    Raises:
        ValueError: If no ID is provided.
    """
    if not id:
        raise ValueError("No id provided")

    posts_to_keep = [post for post in get_blog_posts() if post["id"] != id]
    serialize_blog_posts(posts_to_keep)


def increment_likes(id):
    """
    Increments the likes count of a blog post.

    Args:
        id (int): The ID of the blog post.

    Raises:
        ValueError: If no ID is provided.
        KeyError: If the blog post with the given ID is not found.
    """
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
    """
    Generates the next available ID for a new blog post.

    Args:
        posts (list[dict]): A list of existing blog posts.

    Returns:
        int: The next available ID.
    """
    used_ids = [post["id"] for post in posts]
    id = len(posts)

    while id in used_ids:
        id += 1

    return id
