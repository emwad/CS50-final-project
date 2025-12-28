from flask import Flask, render_template
from helpers import close_db, inst

app = Flask(__name__)

# Register teardown handler
app.teardown_appcontext(close_db)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')
