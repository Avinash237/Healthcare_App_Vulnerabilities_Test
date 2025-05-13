import sqlite3
import os
import pickle
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 1. SQL Injection
@app.route('/user')
def get_user():
    name = request.args.get('name')
    query = f"SELECT * FROM users WHERE name = '{name}'"  # Vulnerable
    conn = sqlite3.connect('users.db')
    result = conn.execute(query).fetchall()
    return str(result)
# Fix: Use parameterized queries

# 2. Cross-Site Scripting (XSS)
@app.route('/search')
def search():
    q = request.args.get('q')
    return render_template_string(f"<h1>You searched for {q}</h1>")  # Vulnerable
# Fix: Sanitize/escape output using Flask templates or bleach

# 3. Hardcoded Credentials
API_KEY = "my_super_secret_key"  # Vulnerable
# Fix: Store in environment variables

# 4. Insecure Deserialization
@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.data
    obj = pickle.loads(data)  # Vulnerable
    return str(obj)
# Fix: Avoid pickle with untrusted data

# 5. Directory Traversal
@app.route('/file')
def get_file():
    filename = request.args.get('filename')
    with open(f"./uploads/{filename}") as f:  # Vulnerable
        return f.read()
# Fix: Sanitize input, use secure filename libraries

if __name__ == "__main__":
    app.run(debug=True)
