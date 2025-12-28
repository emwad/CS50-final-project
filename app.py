from flask import Flask, render_template, request
from helpers import close_db, inst, get_db

app = Flask(__name__)

# Register teardown handler
app.teardown_appcontext(close_db)

@app.route('/', methods=["GET", "POST"])
def index():
    # POST
    if request.method == "POST":
        ukprn = int(request.form.get("inst1"))
        db = get_db()

        # Note - fetchone() brings back 1 row, fetchall() LIST of rows 
        # (so will need cycling through in template)
        # this bit just checking i can bring back the right info for now
        rows = db.execute("SELECT * FROM institutions WHERE ukprn = ?", (ukprn,)).fetchone()
        address = db.execute("SELECT * FROM addresses WHERE ukprn = ?", (ukprn,)).fetchone()
        return render_template('test.html', inst1=rows, inst=address)

    return render_template('index.html')
