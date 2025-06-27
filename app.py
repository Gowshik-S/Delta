from flask import Flask, render_template, request, redirect, jsonify
from main import listen, get_response,greet_st
app = Flask(__name__)

USER = {
    "username": "deltadmin",
    "password": "delta123"
}

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/main')
def home():
    return render_template('delta.html')


@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        return redirect("/main")
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/forgetpassword')
def forgetpassword():
    return render_template('forgetpass.html')

@app.route("/update", methods=["POST"])
def update():
    try:
        data = request.get_json()
        user_msg = data.get("message", "").strip().lower()

        if user_msg:
            assistant_reply = get_response(user_msg)
        else:
            assistant_reply = "Sorry, I didn’t catch that."

        return jsonify({
            "user": user_msg,
            "reply": assistant_reply
        })
    except BaseException as e:
        return jsonify({
            "user": "",
            "reply": f"Error occurred: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True)