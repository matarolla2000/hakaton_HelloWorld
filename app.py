from flask import Flask, request, render_template, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'abcd'

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
        return jsonify({"time": "Введите пароль для анализа надежности", "color": "#626c77"})
        
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)
    
    score = 0
    requirements = []
    
    if length >= 8:
        score += 1
    else:
        requirements.append("минимум 8 символов")
        
    if has_digit:
        score += 1
    else:
        requirements.append("цифры")
        
    if has_upper and has_lower:
        score += 1
    else:
        requirements.append("разный регистр (Аа)")
        
    if has_special:
        score += 1
    else:
        requirements.append("спецсимволы (@#$)")

    if score <= 1:
        status_text = "❌ Критически слабый пароль! Взлом займет до 1 секунды."
        if requirements:
            status_text += " Добавьте: " + ", ".join(requirements)
        color = "#d32f2f"
    elif score == 2 or score == 3:
        status_text = "⚠️ Слабый/Средний пароль. Будет взломан за короткий срок."
        if requirements:
            status_text += " Рекомендуется добавить: " + ", ".join(requirements)
        color = "#f57c00"
    else:
        status_text = "🎯 Идеальный пароль HelloWorld ID! Устойчив к брутфорсу (более 1000 лет)."
        color = "#388e3c"
        
    return jsonify({
        "time": status_text,
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
            "text": "🎯 Отлично! Вы распознали фишинг. Домен helloworld-premium-bonus.ru — поддельный (+5 к рейтингу)",
            "color": "#388e3c",
            "score": "90"
        })
    else:
        return jsonify({
            "text": "❌ Вы попались! Настоящий домен HelloWorld — helloworld.ru. Данные утекли бы хакерам (-10 к рейтингу)",
            "color": "#d32f2f",
            "score": "75"
        })

if __name__ == '__main__':
    app.run(debug=True)