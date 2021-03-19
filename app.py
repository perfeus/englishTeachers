import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# присваиваем значение переменной окружения параметру настроек
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# создаем подключение к БД
db = SQLAlchemy(app)
# создаем объект поддержки миграции
migrate = Migrate(app, db)

teachersGoals = db.Table("teachers_goals",
                         db.Column("teacher_id", db.Integer, db.ForeignKey("teachers.id")),
                         db.Column("goal_id", db.Integer, db.ForeignKey("goals.id")),
                         )


# создаем модель для хранения данных об учителях
class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.relationship("Goal", secondary=teachersGoals, back_populates="teachers")


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    teachers = db.relationship("Teacher", secondary=teachersGoals, back_populates="goals")

@app.route("/all/")
def index():
    tchs = db.session.query(Teacher).all()
    gls = db.session.query(Goal).all()
    teacher = tchs[0].id
    goal = gls[0].goal
    bob = gls[0].teachers
    print(teacher, goal, bob)
    return render_template("all.html", tchs=tchs)

@app.route("/all/rating/", methods=["GET", "POST"])
def allValue():
    if request.method == "POST":
        print(request.form.getlist("myvalue"))
        return "hello {{value}}"



if __name__ == "__main__":
    app.run(debug=True)
