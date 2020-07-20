from flask import Flask, render_template, request, session

# zadefinujeme si nasu Flask aplikaciu
app = Flask(__name__)

# toto by mal byt nejaky nahodny string,
# pouziva sa na sifrovanie sessionov:
app.config["SECRET_KEY"] = "nieco"


@app.route("/", methods=["GET", "POST"])
def ahoj():
    # ak chceme nieco zobrat z POST requestu, pouzijeme request.form
    # ak chceme nieco zobrat z GET requestu (to je ?nieco na konci adresy),
    # pouzijeme request.args
    meno = request.form.get("meno")
    return render_template("formular.html", meno=meno)


# tato "cesta" berie dva parametre: meno a pocet
@app.route("/pozdrav/<meno>/<int:pocet>")
def pozdrav(meno, pocet):
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
