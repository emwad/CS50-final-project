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
        # this bit just checking i can bring back the right info for now
        rows = db.execute("SELECT * FROM nss WHERE ukprn = ?", (ukprn1,)).fetchone()
        rows2 = db.execute("SELECT * FROM nss WHERE ukprn = ?", (ukprn2,)).fetchone()
        plt.barh([rows["PROVIDER_NAME"], rows2["PROVIDER_NAME"]], 
                 [rows["POSITIVITY_MEASURE"], rows2["POSITIVITY_MEASURE"]])
        plt.ylabel("Institution")
        plt.xlabel("Positivity measure") 
        plt.title("Horizontal bar graph")
        chart = plt.show()
        return render_template('comparison.html', inst1=rows, inst2=rows2, chart=chart)

    return render_template('index.html')
