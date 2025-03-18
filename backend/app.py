from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger import setup_swagger
from repository import get_blog_posts, add_blog_post, delete_blog_post, get_blog_post_by_id, \
    update_blog_post, search_blog_posts, sort_blog_posts

app = Flask(__name__)
CORS(app)
setup_swagger(app)


@app.route("/api/posts")
def get_posts():
    sort_field = request.args.get("sort", "")
    sort_direction = request.args.get("direction", "")

    if sort_field or sort_direction:
        try:
            sorted_blog_posts = sort_blog_posts(sort_field.lower(), sort_direction.lower())
            return jsonify(sorted_blog_posts)
        except ValueError as error:
            return jsonify(str(error)), 400

    blog_posts = get_blog_posts()
    return jsonify(blog_posts)


@app.route("/api/posts/search")
def search_posts():
    params = request.args
    search_result = search_blog_posts(**params)
    return jsonify(search_result)


@app.route("/api/posts", methods=["POST"])
def add_post():
    json = request.json

    try:
        new_post = add_blog_post(json.get("author"), json.get("title"), json.get("content"))
        return jsonify(new_post), 201
    except ValueError as error:
        return jsonify(str(error)), 400


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    json = request.json

    try:
        updated_post = update_blog_post(post_id, json.get("author"), json.get("title"),
                                        json.get("content"))
        return jsonify(updated_post)
    except KeyError:
        return jsonify({"message": f"Post with id {post_id} not found."}), 404


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    if not get_blog_post_by_id(post_id):
        return jsonify({"message": f"Post with id {post_id} not found."}), 404

    try:
        delete_blog_post(post_id)
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})
    except ValueError:
        return jsonify({"message": f"Invalid post id {post_id}."}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
