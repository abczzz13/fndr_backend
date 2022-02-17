from flask import jsonify
from app import current_app as app


@app.route("/")
@app.route("/index")
def index():
    return "Under construction"
