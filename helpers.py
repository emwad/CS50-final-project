import sqlite3
from flask import g

DATABASE = "nss.db"

def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Function that takes an institution UKPRN, and a list of theme IDs, 
# and returns an object containing info filtered to that.

def inst(UKPRN, THEME_IDs):
    if not THEME_IDs:
        return []

    db = get_db()

    placeholders = ",".join(["?"] * len(THEME_IDs))
    query = f"SELECT * FROM nss WHERE UKPRN = ? AND THEME_ID IN ({placeholders})"

    rows = db.execute(query, (UKPRN, *THEME_IDs)).fetchall()
    return rows

# encodes a matplotlib chart to base64 string for embedding in HTML
def generate_chart(rows, rows2):
    import io
    import base64
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick

    values = [rows["POSITIVITY_MEASURE"], rows2["POSITIVITY_MEASURE"]]
    labels = [rows["PROVIDER_NAME"], rows2["PROVIDER_NAME"]]

    # Identify highest and lowest
    max_index = values.index(max(values))
    min_index = values.index(min(values))

    # Build colour list
    if max_index == min_index:
        colors = ["#ffc107"] * len(values)  # all same
    else:
        colors = ["#ffc107"] * len(values)
        colors[max_index] = "#198754"    # highest

    fig, ax = plt.subplots()
    ax.barh(labels, values, color=colors)

    ax.set_xlabel("Positivity measure")
    ax.set_xlim(0, 100)

    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.bar_label(ax.containers[0], fmt="%.1f%%")

    fig.set_figheight(2)
    fig.set_figwidth(10)

    # Save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    # Encode
    return base64.b64encode(buf.getvalue()).decode("utf-8")

