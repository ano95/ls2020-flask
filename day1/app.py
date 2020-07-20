from flask import Flask, render_template, request, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "nieco"

@app.route("/", methods=["GET", "POST"])
def ahoj():
    meno = request.form.get("meno")
    return render_template("formular.html", meno=meno)

@app.route("/pozdrav/<meno>/<int:pocet>")
def pozdrav(meno, pocet):
    # pocet = int(pocet)
    return render_template("pozdrav.html", meno=meno, pocet=pocet)


@app.route("/moje_meno")
def moje_meno():
    if "meno" not in session:
        return "nie si prihlaseny"
    return session["meno"]


@app.route("/logout")
def logout():
    del session["meno"]
    return "si odhlaseny."


@app.route("/login", methods=["GET", "POST"])
def login():
    error = False

    if request.method == "POST":
        meno = request.form.get("meno")
        heslo = request.form.get("heslo")

        if meno == "adam" and heslo == "1234":
            session["meno"] = "adam"
            return "hura!"
        else:
            error = "Nespravne meno a heslo."

    return render_template("login.html", error=error)
