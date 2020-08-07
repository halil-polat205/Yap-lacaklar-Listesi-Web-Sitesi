from flask import Flask,render_template, redirect, url_for, session, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_babel import Babel 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/halil/Desktop/Halil/todoapp/data.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
bp = Blueprint('todo', __name__ , url_prefix='/todo' ,template_folder='templates' ,static_folder='static')
app.config["BABEL DEFAULT LOCALE"]='en'
app.secret_key = 'some secret key'
babel = Babel(app)

@app.route("/change_lang")
def change_lang():
    lang =request.args.get("lang")
    if lang not in ["tr","en","de","fr","ar"]:
        lang = "en"
    session["lang"]= lang
    return redirect(url_for("index"))
@babel.localeselector
def language_detector():
    return session["lang"] if "lang" in session else"en"

@app.route("/")
def index():
    todos=Todo.query.all()
    users=user.query.all()   

    return render_template("index.html",todos=todos ,users=users)

@app.route("/add", methods = ["POST","GET"])
def addtodo():

    title = request.form.get("title")
    content = request.form.get("content")
    
    newTodo = Todo(title = title , content = content , Complete = False)
        
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/Delete/<string:id>", methods = ["GET"])
def delete(id):
    todo=Todo.query.filter_by(id=id).first()

    title = request.form.get("title")
    content = request.form.get("content")

    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/Complete/<string:id>",methods =["GET"])
def completetodo(id):
    todo=Todo.query.filter_by(id=id).first()
    
    if  todo.Complete==False:
        todo.Complete=True
    else:
        todo.Complete=False

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/İmportant/<string:id>",methods =["GET"])
def imptodo(id):
    todo=Todo.query.filter_by(id=id).first()
    
    if  todo.İmportant==False:
        todo.İmportant=True
    else:
        todo.İmportant=False

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout",methods=["POST","GET"])
def logout():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.delete(register)
        db.session.commit()

        return redirect(url_for("login"))
    
        todo=Todo.query.filter_by(id=id).first()

        title = request.form.get("title")
        content = request.form.get("content")

        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

    
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    Complete = db.Column(db.Boolean)
    İmportant =db.Column(db.Boolean)


if __name__ == ("__main__"):
    db.create_all()
    app.run(debug=True)
