from flask import Flask, render_template, request
from os import environ
import requests

app = Flask(__name__)

backend_URL = environ.get('BACKEND_URL', 'http://localhost:5001/')
log = []

def get_animals():
    log.append("[FRONTEND] Getting animals from backend")
    return requests.get(url=backend_URL).json()


def add_animal(animal: str, name: str):
    log.append(f"[FRONTEND] Adding Name: {name} Animal: {animal} to database")
    payload = {'name': name, 'animal': animal}
    response = requests.post(backend_URL, data=payload)
    log.append(response.text)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        if request.form.get('get_animals'):
            return render_template("index.html", log=log, animals=get_animals())
        elif request.form.get('add_animal'):
            add_animal(request.form["animal"], request.form["name"])
    return render_template("index.html", log=log)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
