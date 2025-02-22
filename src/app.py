from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

def log_page_load():
    pass

@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html file

@app.route('/set_session', methods=['POST'])
def set_session():
    session['username'] = request.form['username']
    return redirect(url_for('index'))

@app.route('/get_session')
def get_session():
    username = session.get('username', 'Guest')
    return f'Hello, {username}!'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
