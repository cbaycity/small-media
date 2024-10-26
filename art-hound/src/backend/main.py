from flask import Flask


app = Flask(__name__, static_folder="../", static_url_path="/")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/public/<file>")
def public(file):
    return app.send_static_file(f"client/public/{file}")


@app.route("/members")
def members():
    return ["Bayard", "Sean", "Eamon"]


if __name__ == "__main__":
    app.run(debug=True)  # Need to turn off when in production.
