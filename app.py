import os
from operator import itemgetter
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON

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
    schedule = db.Column(JSON)
    goals = db.relationship("Goal", secondary=teachersGoals, back_populates="teachers")
    lesson = db.relationship("Lesson", back_populates="teacher")


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    teachers = db.relationship("Teacher", secondary=teachersGoals, back_populates="goals")


class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)


class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    clientName = db.Column(db.String, nullable=False)
    clientPhone = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher")


@app.route("/all/", methods=["GET", "POST"])
def index():
    tchs = db.session.query(Teacher).all()
    gls = db.session.query(Goal).all()
    return render_template("all.html", data=tchs)


@app.route("/all/sorted/", methods=["GET", "POST"])
def allValue():
    data = list()
    tchs = db.session.query(Teacher).all()
    for item in tchs:
        data.append(dict([("id", item.id),
                          ("name", item.name),
                          ("rating", item.rating),
                          ("price", item.price),
                          ("about", item.about)]))
    if request.method == "POST":
        sortValue = request.form.get("myvalue")
        if sortValue == "1":
            data.sort(key=itemgetter("price"), reverse=True)
            return render_template("all.html", data=data)
        if sortValue == "2":
            data.sort(key=itemgetter("price"), reverse=False)
            return render_template("all.html", data=data)
        if sortValue == "3":
            data.sort(key=itemgetter("rating"), reverse=True)
            return render_template("all.html", data=data)
    return render_template("all.html", data=tchs)


@app.route("/profile/<int:id>/")
def profiles(id):
    teacher = db.session.query(Teacher).get(id)
    return render_template("profile.html", data=teacher)


@app.route("/request/", methods=["GET", "POST"])
def requestAction():
    if request.method == "POST":
        requestGoal = request.form.get("goal")
        requestTime = request.form["time"]
        requestName = request.form["name"]
        requestPhone = request.form["phone"]
        data = [requestGoal, requestTime, requestName, requestPhone]
        entry = Request(goal=requestGoal, time=requestTime, name=requestName, phone=requestPhone)
        db.session.add(entry)
        db.session.commit()
        return render_template("request_done.html", data=data)
    return render_template("request.html")


@app.route("/")
def mainPage():
    teachers = db.session.query(Teacher).all()
    return render_template("index.html", data=teachers)


@app.route("/goal/<goal>/")
def visitorsGoal(goal):
    allGoals = db.session.query(Goal).all()
    if goal == "travel":
        travelGoal = allGoals[0].teachers
        return render_template("goal.html", data=travelGoal, goal="для путешествий")
    if goal == "study":
        travelGoal = allGoals[1].teachers
        return render_template("goal.html", data=travelGoal, goal="для школы")
    if goal == "work":
        travelGoal = allGoals[2].teachers
        return render_template("goal.html", data=travelGoal, goal="для работы")
    if goal == "relocate":
        travelGoal = allGoals[3].teachers
        return render_template("goal.html", data=travelGoal, goal="для переезда")
    return render_template("goal.html")


@app.route("/booking/<teacherId>/<teacherName>/<time>/<day>/", methods=["POST", "GET"])
def bookingAction(teacherId, teacherName, time, day):
    if request.method == "POST":
        clientName = request.form.get("clientName")
        clientPhone = request.form.get("clientPhone")
        data = [clientName, clientPhone]
        teacher = Teacher.query.get(teacherId)
        lesson = Lesson(day=day, time=time, clientName=clientName, clientPhone=clientPhone, teacher=teacher)
        db.session.add(lesson)
        db.session.commit()
        return render_template("booking_done.html", id=teacherId, name=teacherName, time=time, day=day, data=data)
    return render_template("booking.html", id=teacherId, name=teacherName, time=time, day=day)


@app.route("/lessons/")
def lessonsRender():
    return render_template("lessons.html")


if __name__ == "__main__":
    app.run(debug=True)
