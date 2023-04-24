from flask import Flask, render_template

app = Flask(__name__)


@app.route('/login/')
def login():
    return render_template('users/login.html')


@app.route('/registration/')
def registration():
    return render_template('users/registration.html')


if __name__ == '__main__':
    app.run(debug=True)
