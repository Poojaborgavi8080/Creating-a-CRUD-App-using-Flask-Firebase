from flask import Flask, render_template, request, redirect
import pyrebase

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyD0xeakZuqMJEJgomK_ZRcvSNlpJnyzXD4",
  "authDomain": "curd-example-3ce1e.firebaseapp.com",
  "databaseURL": "https://curd-example-3ce1e-default-rtdb.firebaseio.com",
  "projectId": "curd-example-3ce1e",
  "storageBucket": "curd-example-3ce1e.firebasestorage.appspot.com",
  "messagingSenderId": "804450867132",
  "appId": "1:804450867132:web:2f785d38f506743fe77db9",
  "measurementId": "G-31V8CP74S3"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        if name and age:
            db.child("users").push({"name": name, "age": age})
        return redirect("/")
    
    users = db.child("users").get().val()
    return render_template("index.html", users=users)

# UPDATE
@app.route("/update/<string:user_id>", methods=["GET", "POST"])
def update(user_id):
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        db.child("users").child(user_id).update({"name": name, "age": age})
        return redirect("/")
    
    user = db.child("users").child(user_id).get().val()
    return render_template("update.html", user=user, user_id=user_id)

# DELETE
@app.route("/delete/<string:user_id>")
def delete(user_id):
    db.child("users").child(user_id).remove()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)