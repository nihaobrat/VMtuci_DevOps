from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('glavpage.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/lenta')
def lenta():
    return render_template('lenta.html')

@app.route('/createpost')
def create_post():
    return render_template('createpost.html')

@app.route('/createdpost')
def created_post():
    return render_template('createdpost.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)