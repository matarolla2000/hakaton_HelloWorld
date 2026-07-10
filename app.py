from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'any_secret_string_here'
logined = False

@app.route("/")
def index():
    return redirect(url_for("main"))

@app.route("/main")
def main():
    if not session.get('logined', False):
        return redirect(url_for('login'))
    else:
        return render_template("main.html", username=session.get("username"))
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('login').strip()
        password = request.form.get('password').strip()
        session['logined'] = True
        session['username'] = username
        if not username or not password:
            error = "Логин и пароль не могут быть пустыми!"
            return render_template("login.html", error=error)
        return redirect(url_for("main"))
    return render_template("login.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear
    return redirect(url_for("login"))

app.run(debug=True)