Creating a CRUD App using Flask + Firebase

Step 1: Install the required software:
1.	Python (version 3.7 or above) 
2.	pip (comes with Python)
3.	Flask (Python web framework)
4.	Pyrebase (Python library to connect Firebase with Flask
5.	Firebase Account - https://console.firebase.google.com
Step 2: Install Required Python Packages
Open Command Prompt or Terminal and run:
pip install flask pyrebase4
 Step 3: Create Firebase Project
1.	Go to Firebase Console.
2.	Click Add Project → Give it a name (example: curd-example).
3.	Skip Google Analytics (optional).
4.	Once the project is created, click add product then choose
 Realtime Database → Create Database → Choose Start in test mode.
5.	Copy your Firebase Config from Project Settings → General → Your Apps → Web App.
Example Config:
config = {
  "apiKey": "YOUR_API_KEY",
  "authDomain": "yourapp.firebaseapp.com",
  "databaseURL": "https://yourapp-default-rtdb.firebaseio.com",
  "projectId": "yourapp",
  "storageBucket": "yourapp.appspot.com",
  "messagingSenderId": "XXXXXX",
  "appId": "XXXXXXXXXXXXXX"
}

Step 4: Project Structure
flask_firebase_crud
│-- app.py               # Main Flask app
│-- templates 
│    │-- index.html       # Homepage with form + user list
│    │-- update.html      # Update user form

Step 5: curdEx.py

1. Importing Required Libraries
from flask import Flask, render_template, request, redirect
import pyrebase
•	Flask → The Python web framework we’re using to create the web server.
•	render_template → Loads HTML files from the templates/ folder.
•	request → Lets us read data sent by the user (form inputs).
•	redirect → Sends the user to another page after an action.
•	pyrebase → Library that connects Python to Firebase.
2. Flask App Setup
app = Flask(__name__)
•	Creates a Flask app object so we can define routes (pages).

3. Firebase Configuration
config = {
  "apiKey": "YOUR_API_KEY",
  "authDomain": "yourapp.firebaseapp.com",
  "databaseURL": "https://yourapp-default-rtdb.firebaseio.com",
  "projectId": "yourapp",
  "storageBucket": "yourapp.appspot.com",
  "messagingSenderId": "XXXXXX",
  "appId": "XXXXXXXXXXXXXX"
}
•	This dictionary contains all the credentials to connect our Flask app to Firebase.
•	You get these from Firebase Console → Project Settings → Your Apps.
4. Connect to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()
•	initialize_app(config) → Starts Firebase with our config.
•	.database() → Connects to Realtime Database.

5. Home Page Route (Create + Read)
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
•	@app.route("/", methods=["GET", "POST"]) → This is the home page.
•	When method is POST (form is submitted):
o	Read name and age from the form.
o	.push() → Adds a new user to Firebase under users.
o	redirect("/") → Reloads the page after adding.
•	When method is GET (page is just loaded):
o	.get().val() → Fetches all users from Firebase.
o	render_template() → Sends data to index.html for display.

6. Update User Route
@app.route("/update/<string:user_id>", methods=["GET", "POST"])
def update(user_id):
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        db.child("users").child(user_id).update({"name": name, "age": age})
        return redirect("/")
    
    user = db.child("users").child(user_id).get().val()
    return render_template("update.html", user=user, user_id=user_id)
•	/<string:user_id> → This part of the URL captures the Firebase user’s ID.
•	When POST:
o	Update that specific user in Firebase with new name and age.
•	When GET:
o	Fetch user’s current data.
o	Show it in the update.html form so we can edit.

7. Delete User Route
@app.route("/delete/<string:user_id>")
def delete(user_id):
    db.child("users").child(user_id).remove()
    return redirect("/")
•	.remove() deletes the user with that ID from Firebase.
•	After deletion, we redirect back to the home page.

8. Run the App
if __name__ == "__main__":
    app.run(debug=True)
•	Runs the Flask app.
•	debug=True → Automatically reloads when code changes & shows detailed error messages.

