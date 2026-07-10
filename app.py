from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'any_secret_string_here'
logined = False

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты дружелюбный и краткий ассистент в чате."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Извлекаем текст ответа
        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": f"Ошибка API: {str(e)}"}), 500

app.run(debug=True)