from enum import unique
from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/crud_ops'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


@app.route('/')
def index():
    my_data = User.query.all()
    return render_template('index.html', table=my_data)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        data = request.form
        username = data['name']
        email = data['email']
        ops = data['act']

        if ops == 'create':
            my_data = User(username, email)
            db.session.add(my_data)
            db.session.commit()

        elif ops == 'update':
            id = int(data['id'])
            my_data = User.query.get(id)
            my_data.username = username
            my_data.email = email
            db.session.commit()

        return redirect(url_for('index'))

@app.route('/delete/<id>',methods=['POST', 'GET'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)