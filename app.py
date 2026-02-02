from flask import Flask, jsonify, render_template, request
from helpers import close_db, generate_chart, get_db

app = Flask(__name__)

# Register teardown handler. This was suggested by Microsoft Copilot AI, when querying
# how to properly open and close database connections in Flask.
app.teardown_appcontext(close_db)

@app.route('/', methods=["GET", "POST"])
def index():
    db = get_db()
    #POST
    if request.method == "POST":
        ukprn1 = int(request.form.get("inst1_id"))
        ukprn2 = int(request.form.get("inst2_id"))
        themes = [int(t) for t in request.form.getlist("themes[]")]

        if not themes or not ukprn1 or not ukprn2:
            providers = db.execute("SELECT DISTINCT PROVIDER_NAME, UKPRN FROM nss ORDER BY PROVIDER_NAME").fetchall()
            provider_list = [{"name": row["PROVIDER_NAME"], "ukprn": row["UKPRN"]} for row in providers]
            return render_template('index.html', providers=provider_list, message="Please select two institutions and at least one theme to compare.")

        theme_info = [None] * len(themes)
        charts = [None] * len(themes)

        # Microsoft Copilot AI suggested the 'enumerate' function during error checking
        for i, theme in enumerate(themes):
            temp1 = db.execute("SELECT * FROM nss WHERE SUBJECT_LEVEL = 'All subjects' AND ukprn = ? AND theme_id = ?", (ukprn1, theme)).fetchone()
            temp2 = db.execute("SELECT * FROM nss WHERE SUBJECT_LEVEL = 'All subjects' AND ukprn = ? AND theme_id = ?", (ukprn2, theme)).fetchone()

            if temp1 is None or temp2 is None:
                return render_template('index.html', providers=provider_list, message=f"Theme {theme} not available for one or both institutions.")

            theme_info[i] = db.execute(
                "SELECT theme_id, question_number FROM themes WHERE theme_id = ?",
                (theme,)
            ).fetchone()

            charts[i] = generate_chart(temp1, temp2)

        return render_template("comparison.html", themes=theme_info, charts=charts)

    #GET
    providers = db.execute("SELECT DISTINCT(PROVIDER_NAME), UKPRN FROM nss ORDER BY PROVIDER_NAME").fetchall()
    provider_list = [{"name": row["PROVIDER_NAME"], "ukprn": row["UKPRN"]} for row in providers]
    return render_template('index.html', providers=provider_list)

# Further info on NSS Themes and Positivity Measure.
@app.route("/info")
def info():
    return render_template("info.html")

# Autocomplete function on the user form. Microsoft Copilot AI assisted in tweaking this function after I initially wrote it.
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