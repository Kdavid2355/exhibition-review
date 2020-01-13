from flask import (
    Flask,
    session,
    redirect,
    url_for,
    escape,
    request,
    render_template,
    jsonify)
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "qwertyu"
client = MongoClient(
    "mongodb+srv://bjk:helloworld@heewon-fyhwo.gcp.mongodb.net/test?retryWrites=true&w=majority"
)
db = client.bjk


@app.route("/")
def home():
    userid = session.get("userid", None)
    exhibition = db.exhibitions.find()
    return render_template("home.html", userid=userid, data=exhibition)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    userid_receive = request.form["userid"]
    password_receive = request.form["password"]
    result_id = db.users.find_one({"password": password_receive})
    try:
        if (
            userid_receive == result_id["userid "]
            and password_receive == result_id["password"]
        ):
            session["userid"] = request.form["userid"]
            return redirect("/")
    except TypeError:
        print("다시입력하세요!")
        return render_template("login.html")

    # print(db.users.find({},{'_id':0},{'userid':userid_receive, 'password':password_receive}))
    # print(result_id['userid '])
    # if userid_receive == result_id['userid '] and password_receive == result_id('password'):
    #     return render_template('home.html')
    #     #return render_template('home.html')

    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    userid = request.form["userid"]
    password = request.form["password"]
    repassword = request.form["re-password"]
    if password == repassword:
        doc = {"userid ": userid, "password": password}
        db.users.insert_one(doc)
        session["userid"] = userid
        print("SUCCESS")
        return redirect("/")
    return render_template("register.html")


@app.route("/review/<exid>", methods=["POST", "GET"])
def review(exid):
    if request.method == "GET":
        exhibition = db.exhibitions.find_one({"_id": ObjectId(exid)})
        review = db.review.find({"ex_id": ObjectId(exid)})
        return render_template("review.html", exhibition=exhibition, review=review)
    else:
        score = request.form["score"]
        review = request.form["review"]
        doc = {"score": score, "review": review, "ex_id": ObjectId(exid)}
        db.review.insert_one(doc)
        print("SUCCESS")
        return redirect("/review/"+exid)


if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug=True)
