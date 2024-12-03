from flask import *
import json


app = Flask(__name__)


@app.route('/')
def index():
    with open("blog_data.json", "r") as fileobj:
        blog_posts = json.load(fileobj)
        for blog in blog_posts:
            print(blog)
    if request.method == 'POST':
        return redirect(url_for("add.html"))
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        new_post = request.form.get()
        return redirect(url_for("index.html"))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

