#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route('/states/<id>', strict_slashes=False)
def state_id(id):
    """display a HTML page with info about <id>, if it exists."""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html')


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
