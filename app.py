
from flask import Flask, render_template, request, redirect, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import bcrypt
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:8889/flask_web"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = 'static/uploads'

#mail code

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '48a4bddcc0af2c'
app.config['MAIL_PASSWORD'] = '485c6a0a1869ae'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False



db = SQLAlchemy(app)
mail = Mail(app)
app.secret_key = 'secret_key'

class admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True)
    mobile = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100))
    image = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Integer, nullable=True)
    # date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name, email, image, password, mobile, status):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.image = image
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
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

#image upload
        image = request.files['img']
        if image:
            filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#mail code
        subject = "Test mail"
        message_body = "this is a testing mail"

        msg = Message(subject=subject, sender="vishalarora1087@gmail.com", recipients=["vishalarora1087@gmail.com", "hello"])
        msg.body = message_body
        mail.send(msg)

        '''try:
            mail.send(msg)
            return "email send successfully!"
        except Exception as e:
            return "Error sending email : " + str(e)'''

        admin_entry = admins(name=name, mobile=mobile, image=filename, email=email, password=password, status=status)
        db.session.add(admin_entry)
        db.session.commit()
        return redirect('admin_login')

    return render_template('admin_register.html')

@app.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = admins.query.filter_by(email=email).first()

        if admin and admin.check_password(password):
            #session['name'] = admin.name
            session['email'] = admin.email
            #session['password'] = admin.password
            return redirect('/dashboard')
        else:
            return render_template('admin_register.html', error='Invalid user')

    return render_template('admin_login.html')


@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        admin_dash = admins.query.filter_by(email=session['email']).first()
        return render_template('admin_dash/dashboard.html', admin_dash=admin_dash)
    return redirect('/admin_login')

@app.route('/logout')
def admin_logout():
    session.pop('email',None)
    return redirect('/')

@app.route('/download/<int:file_id>')
def download(file_id):
    file = admins.query.get_or_404(file_id)
    return (send_from_directory(app.config['UPLOAD_FOLDER'], file.image, as_attachment=True))

@app.route('/delete/<int:file_id>')
def delete(file_id):
    file = admins.query.get_or_404(file_id)
    filename = file.image
    file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    os.remove(file_path)
    db.session.delete(file)
    db.session.commit()
    return redirect('/dashboard')


if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)