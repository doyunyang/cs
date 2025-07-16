from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = 'mysecret'

CSV_FILE = 'users.csv'

def save_user(username, password):
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password])

def load_users():
    if not os.path.exists(CSV_FILE):
        return []

    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

# 홈
@app.route('/')
def home():
    return render_template('home.html')

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        for user in users:
            if user['username'] == username:
                return '이미 존재하는 아이디입니다.'

        save_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('profile'))

        return '로그인 실패!'

    return render_template('login.html')

# 프로필
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['username'])

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/users')
def user_list():
    users = load_users()
    return '<br>'.join([user['username'] for user in users])

if __name__ == '__main__':
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password'])
            writer.writerow(['admin', '1216'])
    app.run(debug=True)
