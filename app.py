from flask import Flask, render_template
from repository import get_blog_posts

app = Flask(__name__)


@app.route("/")
def index():
    blog_posts = get_blog_posts()
    return render_template("index.html", blogs=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
