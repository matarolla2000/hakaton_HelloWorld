from flask import Flask, request, render_template, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'any_secret_string_here'

@app.route("/")
def index():
    return redirect(url_for("main"))

@app.route("/main")
def main():
    if not session.get('logined'):
        return redirect(url_for('login'))
    return render_template("main.html", username=session.get("username"))
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('login', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            error = "Логин и пароль не могут быть пустыми!"
            return render_template("login.html", error=error)
            
        session['logined'] = True
        session['username'] = username
        return redirect(url_for("main"))
    return render_template("login.html")

@app.route("/test")
def test():
    if not session.get('logined'):
        return redirect(url_for('login'))
    return render_template("test.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/check_password", methods=["POST"])
def check_password():
    if not session.get('logined'):
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.get_json() or {}
    password = data.get("password", "")
    length = len(password)
    
    if length == 0:
        return jsonify({"time": "Введите пароль, чтобы узнать время взлома", "color": "#88929c"})
        
    time_to_crack = "0 секунд"
    color = "#ff4d4d"
    
    if 0 < length < 6:
        time_to_crack = "Мгновенно (менее 1 секунды)"
    elif 6 <= length < 9:
        time_to_crack = "Около 2 минут"
    elif 9 <= length < 12:
        time_to_crack = "Примерно 5 дней"
        color = "#ffb300"
    elif length >= 12:
        has_upper = any(char.isupper() for char in password)
        has_digit = any(char.isdigit() for char in password)
        
        if has_upper and has_digit:
            time_to_crack = "Более 400 лет (Отличная защита!)"
            color = "#2efd4c"
        else:
            time_to_crack = "Около 3 месяцев"
            color = "#ffb300"
            
    return jsonify({
        "time": f"Время взлома хакерами: {time_to_crack}",
        "color": color
    })

@app.route("/check_phish", methods=["POST"])
def check_phish():
    if not session.get('logined'):
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.get_json() or {}
    is_reported = data.get("is_reported", False)
    
    if is_reported:
        return jsonify({
            "text": "🎯 Отлично! Вы распознали фишинг. Домен mts-premium-bonus.ru — поддельный (+5 к рейтингу)",
            "color": "#2efd4c",
            "score": "90"
        })
    else:
        return jsonify({
            "text": "❌ Вы попались! Настоящий домен МТС — mts.ru. Данные утекли бы хакерам (-10 к рейтингу)",
            "color": "#ff4d4d",
            "score": "75"
        })

if __name__ == '__main__':
    app.run(debug=True)