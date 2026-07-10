from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


logined = False
@app.route("/")
def index():
    return redirect(url_for("main"))

@app.route("/main")
def main():
    if logined == True:
        return render_template("main.html")
    else:
        return login()
    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/test")
def test():
    return render_template("test.html")