from flask import Flask,request,redirect,url_for, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db =SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100),unique=True)
    password =db.Column(db.String(200))
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        username=request,form['username']
        password=request,form['password']
        new_user = User(username=username,
                        password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('register.html')
if __name__=="__main__":
    app.run(debug=True)