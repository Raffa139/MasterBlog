from flask import Flask, jsonify
from flask_cors import CORS
from repository import get_blog_posts

app = Flask(__name__)
CORS(app)


@app.route("/api/posts")
def get_posts():
    blog_posts = get_blog_posts()
    return jsonify(blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
