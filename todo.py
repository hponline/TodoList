from flask import Flask, render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

# SqlAlchemy Konfigürasyon
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Apo/Desktop/Python Ders/TodoApp/todo.db'
db = SQLAlchemy(app)

# Tablo Oluşturma
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)


# Anasayfa
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos=todos)


@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    # Tersini Alır True/False
    todo.complete = not todo.complete
    db.session.commit()

    return redirect(url_for("index"))

# Todo Ekle
@app.route("/add", methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

# Todo Sil
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))


# Flask uygulama bağlamınını ayarlar ve veritabanı tablolarını oluşturur. Silince hata veriyor.
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    
    app.run(debug=True)