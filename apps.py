#import important libraries
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
app.config['SECRET_KEY']="f9bf78b9a18ce6d46a0cd2b0b86df9da"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column("student_id", db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    addr = db.Column(db.String(300))
    clg = db.Column(db.String(300))
    cgpa = db.Column(db.Integer)
    city = db.Column(db.String(300))
    pin  = db.Column(db.Integer)

    def __init__(self, name, addr, clg, cgpa, city, pin):
        self.name = name
        self.addr = addr
        self.clg = clg
        self.cgpa = cgpa
        self.city = city
        self.pin  = pin
    
    def __repr__(self):
        return self.name

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html", data=Student.query.all())


@app.route("/new", methods=['GET','POST'])
def new_entry():
    if request.method=="POST":
        #print(request.form)
        if not request.form['name'] or not request.form['addr'] or not request.form['city'] or not request.form['pin'] or not request.form['clg'] or not request.form['cgpa']:
            flash("Please enter all required fields", "error")
        else:
            std=Student(request.form['name'],request.form['addr'], request.form['city'], request.form['pin'], request.form['clg'], request.form['cgpa'])
            db.session.add(std)
            db.session.commit()
            flash("Record added successfully!")
            return redirect(url_for("home"))
    else:
        return render_template("new_entry.html")

@app.route("/update/<sid>", methods=['GET','POST'])
def update(sid=1):
    if request.method=="POST":
        if not request.form['name'] or not request.form['addr'] or not request.form['city'] or not request.form['pin'] or not request.form['clg'] or not request.form['cgpa']:
            flash("Please enter all required fields", "error")
        else:
            new_name=request.form['name']
            new_addr=request.form['addr']
            new_city=request.form['city']
            new_pin=request.form['pin']
            new_clg=request.form['clg']
            new_cgpa=request.form['cgpa']

            std=Student.query.get(sid)
            std.name=new_name
            std.addr=new_addr
            std.city=new_city
            std.pin=new_pin
            std.clg=new_clg
            std.cgpa=new_cgpa
            db.session.add(std)
            db.session.commit()
            flash("Information Updated Successfully!")
            return redirect(url_for("home"))
    else:
        return render_template("update.html")

@app.route("/delete/<int:sid>", methods=['POST','GET'])
def delete_data(sid):
    std=Student.query.get(sid)
    if std:
        db.session.delete(std)
        db.session.commit()
        flash("Record Deleted Successfully!")
    else:
        flash("Student not found")
    return redirect(url_for("home"))

























if __name__=="__main__":
    
    db.create_all()
    app.run(debug=True)