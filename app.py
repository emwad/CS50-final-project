from flask import Flask, render_template, request
from helpers import close_db, inst, get_db
import matplotlib.pyplot as plt

app = Flask(__name__)

# Register teardown handler
app.teardown_appcontext(close_db)

@app.route('/', methods=["GET", "POST"])
def index():
    # POST
    if request.method == "POST":
        ukprn1 = int(request.form.get("inst1"))
        ukprn2 = int(request.form.get("inst2"))
        db = get_db()

        # Note - fetchone() brings back 1 row, fetchall() LIST of rows 
        # (so will need cycling through in template)

        import io
        import base64
        import matplotlib.pyplot as plt

        rows = db.execute("SELECT * FROM nss WHERE ukprn = ?", (ukprn1,)).fetchone()
        rows2 = db.execute("SELECT * FROM nss WHERE ukprn = ?", (ukprn2,)).fetchone()

        # Create the figure
        fig, ax = plt.subplots()
        ax.barh(
            [rows["PROVIDER_NAME"], rows2["PROVIDER_NAME"]],
            [rows["POSITIVITY_MEASURE"], rows2["POSITIVITY_MEASURE"]]
        )
        ax.set_ylabel("Institution")
        ax.set_xlabel("Positivity measure")
        ax.set_title("Horizontal bar graph")

        # Save to buffer
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)

        # Encode
        chart = base64.b64encode(buf.getvalue()).decode("utf-8")

        return render_template("comparison.html", inst1=rows, inst2=rows2, chart=chart)

    return render_template('index.html')
