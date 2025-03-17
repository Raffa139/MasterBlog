from flask import Flask, render_template, request, redirect, url_for
from repository import get_blog_posts, get_blog_post_by_id, add_blog_post, update_blog_post, \
    delete_blog_post, increment_likes

app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the index page with a list of blog posts.
    """
    blog_posts = get_blog_posts()
    return render_template("index.html", blogs=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Handles adding a new blog post.

    If the request method is POST, it retrieves form data, adds the blog post,
    and redirects to the index page.

    If the request method is GET, it renders the add blog post form.
    """
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        try:
            add_blog_post(author, title, content)
        except ValueError:
            return "Bad request", 400

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """
    Handles updating an existing blog post.

    If the request method is POST, it retrieves form data, updates the blog post,
    and redirects to the index page.

    If the request method is GET, it retrieves the blog post by ID and renders the update form.

    Args:
        post_id (int): The ID of the blog post to update.
    """
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        try:
            update_blog_post(post_id, author, title, content)
        except KeyError:
            return "Not found", 404
        except ValueError:
            return "Bad request", 400

        return redirect(url_for("index"))

    post = get_blog_post_by_id(post_id)
    if not post:
        return "Not found", 404

    return render_template("update.html", post=post)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """
    Handles deleting a blog post.

    Args:
        post_id (int): The ID of the blog post to delete.
    """
    try:
        delete_blog_post(post_id)
    except ValueError:
        return "Bad request", 400

    return redirect(url_for("index"))


@app.route("/like/<int:post_id>")
def like(post_id):
    """
    Handles incrementing the likes count of a blog post.

    Args:
        post_id (int): The ID of the blog post to like.
    """
    try:
        increment_likes(post_id)
    except KeyError:
        return "Not found", 404
    except ValueError:
        return "Bad request", 400

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
