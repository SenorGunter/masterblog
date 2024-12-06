from flask import *
import json
import uuid

app = Flask(__name__)


def load_data():
    with open("blog_data.json", "r") as fileobj:
        data = json.load(fileobj)
    return data


def generate_uid():
    return str(uuid.uuid4())


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Home site """
    blog_posts = load_data()

    if request.method == 'POST':
        action = request.form.get("action")
        post_id = request.form.get("post_id")

        if action == "add":
            return redirect(url_for("add"))
        elif action == "update":
            return redirect(url_for("update", post_id=post_id))

    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=["GET", "POST"])
def add():
    """ Function to add a new blog entry """

    if request.method == 'POST':
        blog_author = request.form.get("author")
        blog_title = request.form.get("title")
        blog_content = request.form.get("content")

        unique_id = generate_uid()

        data = load_data()

        new_data = {"id": unique_id, "author": blog_author, "title": blog_title, "content": blog_content}

        data.append(new_data)
        with open("blog_data.json", "w") as fileobj:
            json.dump(data, fileobj)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route("/delete/<post_id>", methods=["GET", "POST"])
def delete(post_id):
    """ Delete a post and reload the site with updated data"""
    post_to_delete = None
    data = load_data()

    for post in data:
        if post_id == post.get("id"):
            post_to_delete = post
            break

    if post_to_delete:
        data.remove(post_to_delete)
        with open("blog_data.json", "w") as fileobj:
            json.dump(data, fileobj)
        print("Post deleted")
    else:
        print("404: ID not found")

    return render_template("index.html", posts=data)


@app.route("/update/<post_id>", methods=["GET", "POST"])
def update(post_id):
    data = load_data()
    post_to_update = None

    for post in data:
        if post_id == post.get("id"):
            post_to_update = post
            break

    print(post_to_update)
    if post_to_update is None:
        return "Post not found", 404

    if request.method == 'POST':
        updated_author = request.form.get("author")
        updated_title = request.form.get("title")
        updated_content = request.form.get("content")

        post_to_update['author'] = updated_author
        post_to_update['title'] = updated_title
        post_to_update['content'] = updated_content

        with open("blog_data.json", "w") as fileobj:
            json.dump(data, fileobj)
        return render_template("index.html", posts=data)

    return render_template('update.html', post=post_to_update)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

