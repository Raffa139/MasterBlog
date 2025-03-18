import json
import os

REPOSITORY_FILE = "data/blog-posts.json"


def initialize():
    if not os.path.exists(REPOSITORY_FILE):
        with open(REPOSITORY_FILE, mode="x", encoding="utf-8") as file:
            pass


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
    try:
        return deserialize_blog_posts()
    except json.decoder.JSONDecodeError:
        return []


def get_blog_post_by_id(id):
    """
    Retrieves a blog post by its ID.

    Args:
        id (int): The ID of the blog post.

    Returns:
        dict or None: A dictionary representing the blog post, or None if not found.
    """
    try:
        post_by_id, = [post for post in get_blog_posts() if post["id"] == id]
        return post_by_id
    except ValueError:
        return None


def sort_blog_posts(sort_field, sort_direction):
    blog_posts = get_blog_posts()

    if not blog_posts:
        return []

    if sort_field not in blog_posts[0] or sort_direction not in ["asc", "desc"]:
        raise ValueError({
            "invalid-sort-options": {
                "sort": sort_field not in blog_posts[0],
                "direction": sort_direction not in ["asc", "desc"]
            }
        })

    return sorted(blog_posts, key=lambda post: post[sort_field], reverse=sort_direction == "desc")


def search_blog_posts(**search_fields):
    blog_posts = get_blog_posts()
    search_results = []

    if not search_fields:
        return blog_posts

    for post in blog_posts:
        for search_field, search_value in search_fields.items():
            if search_field in post.keys():
                value = post.get(search_field)

                if not isinstance(value, str):
                    continue

                if post in search_results:
                    search_results.remove(post)

                if search_value.lower() in value.lower():
                    search_results.append(post)

    return search_results


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
        raise ValueError({
            "missing-fields": {
                "author": not author,
                "title": not title,
                "content": not content
            }
        })

    blog_posts = get_blog_posts()
    id = next_id(posts=blog_posts)

    new_post = {
        "id": id,
        "author": author,
        "title": title,
        "content": content,
        "likes": 0
    }

    blog_posts.append(new_post)
    serialize_blog_posts(blog_posts)
    return new_post


def increment_likes(id):
    """
    Increments the likes count of a blog post.

    Args:
        id (int): The ID of the blog post.

    Raises:
        ValueError: If no ID is provided.
        KeyError: If the blog post with the given ID is not found.
    """
    if id is None:
        raise ValueError("No id provided")

    post = get_blog_post_by_id(id)

    if not post:
        raise KeyError()

    return update_blog_post(id, post.get("author"), post.get("title"), post.get("content"),
                            post.get("likes") + 1)


def update_blog_post(id, author=None, title=None, content=None, likes=None):
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
    blog_posts = get_blog_posts()
    old_post = get_blog_post_by_id(id)

    if not old_post:
        raise KeyError()

    updated_post = {
        "id": id,
        "author": author if author else old_post["author"],
        "title": title if title else old_post["title"],
        "content": content if content else old_post["content"],
        "likes": likes if likes else old_post["likes"]
    }

    blog_posts.remove(old_post)
    blog_posts.append(updated_post)
    serialize_blog_posts(blog_posts)
    return updated_post


def delete_blog_post(id):
    """
    Deletes a blog post from the repository.

    Args:
        id (int): The ID of the blog post to delete.

    Raises:
        ValueError: If no ID is provided.
    """
    if id is None:
        raise ValueError("No id provided")

    posts_to_keep = [post for post in get_blog_posts() if post["id"] != id]
    serialize_blog_posts(posts_to_keep)


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
