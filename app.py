from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель данных
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    dietary = db.Column(db.Text, nullable=True)
    drinks = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Survey {self.name} ({self.guests} гостей)>"

# Инициализация базы данных
@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()  # Получаем данные в формате JSON
        name = data.get("name")
        guests = data.get("guests")
        dietary = data.get("dietary")
        drinks = data.get("drinks")

        # Проверка обязательных полей
        if not name or not guests:
            return jsonify({"error": "Имя и количество гостей обязательны!"}), 400

        # Преобразование количества гостей в целое число
        guests = int(guests)

        # Преобразование списка напитков в строку
        drinks_str = ", ".join(drinks)

        # Добавление данных в базу
        new_entry = Survey(name=name, guests=guests, dietary=dietary, drinks=drinks_str)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"success": "Ваш ответ успешно сохранён!"}), 200
    except ValueError as ve:
        db.session.rollback()  # Откат изменений в случае ошибки
        return jsonify({"error": f"Ошибка преобразования данных, обратитесь к админу: {ve}"}), 400
    except Exception as e:
        db.session.rollback()  # Откат изменений в случае ошибки
        return jsonify({"error": f"Произошла ошибка, обратитесь к админу: {e}"}), 500

@app.route("/data")
def view_data():
    try:
        rows = Survey.query.all()  # Получение всех данных
        return render_template("data.html", rows=rows)
    except Exception as e:
        flash(f"Произошла ошибка, обратитесь к админу: {e}", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)