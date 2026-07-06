from flask import Flask, render_template, request, redirect
import json
import random
import string
from flask import url_for
import os

app = Flask(__name__)


def load_links():
    try:
        with open("links.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_links(data):
    with open("links.json", "w") as file:
        json.dump(data, file, indent=4)


def generate_code():

    characters = string.ascii_letters + string.digits

    return "".join(random.choices(characters, k=6))


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten():

    original_url = request.form["url"].strip()

    if original_url == "":
        return render_template(
            "index.html",
            error="Please enter a URL."
        )

    if not (
        original_url.startswith("http://")
        or
        original_url.startswith("https://")
    ):
        return render_template(
            "index.html",
            error="URL must start with http:// or https://"
        )

    links = load_links()

    code = generate_code()

    while any(link["code"] == code for link in links):
        code = generate_code()

    links.append(
        {
            "code": code,
            "url": original_url,
            "clicks": 0
        }
    )

    save_links(links)

    short_url = url_for(
    "redirect_short_url",
    code=code,
    _external=True
)

    return render_template(
    "index.html",
    short_url=short_url,
    original_url=original_url
)

@app.route("/dashboard")
def dashboard():

    links = load_links()

    return render_template(
        "dashboard.html",
        links=links
    )


@app.route("/s/<code>")
def redirect_short_url(code):

    links = load_links()

    for link in links:

        if link["code"] == code:

            link["clicks"] += 1

            save_links(links)

            return redirect(link["url"])

    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )