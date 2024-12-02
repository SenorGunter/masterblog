from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open("blog_data.json", "r") as fileobj:
        blog_posts = fileobj.readlines()
        for blog in blog_posts:
            print(blog)
    return render_template("index.html", posts="blog_data")


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

