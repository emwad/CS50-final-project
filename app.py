from flask import Flask, jsonify, render_template, request
from helpers import close_db, generate_chart, inst, get_db
import matplotlib.pyplot as plt

app = Flask(__name__)

# Register teardown handler
app.teardown_appcontext(close_db)

@app.route('/', methods=["GET", "POST"])
def index():
    db = get_db()
    #POST
    if request.method == "POST":
        ukprn1 = int(request.form.get("inst1_id"))
        ukprn2 = int(request.form.get("inst2_id"))

        row = db.execute("SELECT * FROM nss WHERE ukprn = ?", (ukprn1,)).fetchone()
        row2 = db.execute("SELECT * FROM nss WHERE ukprn = ?", (ukprn2,)).fetchone()

        chart = generate_chart(row, row2)

        return render_template("comparison.html", inst1=row, inst2=row2, chart=chart)

    #GET
    providers = db.execute("SELECT DISTINCT(PROVIDER_NAME), UKPRN FROM nss ORDER BY PROVIDER_NAME").fetchall()
    provider_list = [{"name": row["PROVIDER_NAME"], "ukprn": row["UKPRN"]} for row in providers]
    return render_template('index.html', providers=provider_list)

@app.route("/autocomplete")
def autocomplete():
    db = get_db()
    q = request.args.get("q", "")
    rows = db.execute(
        "SELECT ukprn, provider_name FROM institutions WHERE provider_name LIKE ? LIMIT 10",
        (f"%{q}%",)
    ).fetchall()

    return jsonify([
        {"ukprn": row["ukprn"], "name": row["provider_name"]}
        for row in rows
    ])

