from flask import Flask, render_template, session, request
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "sem si daj nahodny secret"


@app.route("/", methods=["GET", "POST"])
def index():
    sprava = ""

    if "cislo" not in session:
        # nemame cislo, vygeneruj nove
        session["cislo"] = random.randint(0, 100)

    if request.method == "POST":
        tip = int(request.form.get("cislo"))
        if tip < session["cislo"]:
            sprava = "Cislo je vacsie."
        elif tip > session["cislo"]:
            sprava = "Cislo je mensie."
        else:
            # po skonceni hry vygenerujeme nove
            sprava = "Uhadol si!"
            session["cislo"] = random.randint(0, 100)

    return render_template("index.html", sprava=sprava)
