from flask import Flask, jsonify, request
from flask_cors import CORS
from repository import get_blog_posts, add_blog_post

app = Flask(__name__)
CORS(app)


@app.route("/api/posts")
def get_posts():
    blog_posts = get_blog_posts()
    return jsonify(blog_posts)


@app.route("/api/posts", methods=["POST"])
def add_post():
    json = request.json

    try:
        new_post = add_blog_post(json.get("author"), json.get("title"), json.get("content"))
        return jsonify(new_post), 201
    except ValueError as error:
        return jsonify(str(error)), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
