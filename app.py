from flask import Flask, request
import sqlite3
import subprocess
import os

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret (Gitleaks/TruffleHog will catch this)
SECRET_KEY = "supersecretpassword123"
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"

# VULNERABILITY 2: SQL Injection (Bandit/Semgrep will catch this)
@app.route('/user')
def get_user():
username = request.args.get('username')
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
return str(cursor.fetchall())

# VULNERABILITY 3: Command Injection (Bandit/Semgrep will catch this)
@app.route('/ping')
def ping():
host = request.args.get('host')
result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True)
return result.stdout.decode()

@app.route('/')
def home():
return "Welcome to Baypitch!"

if __name__ == '__main__':
app.run(debug=True, host='0.0.0.0')
