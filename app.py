from flask import Flask, render_template 
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/job/apply')
def job_apply():
    return render_template('job_details.html')

@app.route('/admin_register')
def admin_register():
    return render_template('admin_register.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)