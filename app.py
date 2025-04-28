from flask import Flask, render_template, request, redirect, url_for
from db_helper import DBHelper

app = Flask(__name__)
db = DBHelper()

@app.route('/')
def home():
    users = db.fetch_all()
    return render_template('index.html', users=users)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        userId = request.form['userId']
        userName = request.form['userName']
        phone = request.form['phone']
        db.insert_user(userId, userName, phone)
        return redirect(url_for('home'))
    return render_template('insert.html')

@app.route('/update/<int:userId>', methods=['GET', 'POST'])
def update(userId):
    if request.method == 'POST':
        newName = request.form['userName']
        newPhone = request.form['phone']
        db.update_user(userId, newName, newPhone)
        return redirect(url_for('home'))
    return render_template('update.html', userId=userId)

@app.route('/delete/<int:userId>')
def delete(userId):
    db.delete_user(userId)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
