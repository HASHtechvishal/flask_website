from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:8889/flask_web"
db = SQLAlchemy(app)

class admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True)
    mobile = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100))
    # image = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Integer, nullable=True)
    # date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name, email, password, mobile, status):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #getsalt()
        self.status = status

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/job/apply')
def job_apply():
    return render_template('job_details.html')

@app.route('/admin_register', methods = ['GET','POST'])
def admin_register():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        status = 1
        #img = request.form.get('img')
        admin_entry = admins(name=name, mobile=mobile, email=email, password=password, status=1)
        db.session.add(admin_entry)
        db.session.commit()
        return redirect('admin_login')

    return render_template('admin_register.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)