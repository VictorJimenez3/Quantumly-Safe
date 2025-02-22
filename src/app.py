from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

def log_page_load():
    pass

@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html file

@app.route('/signup')
def signup():
    return render_template('signup.html')  # Render the signup.html file
    
@app.route('/set_session', methods=['POST'])
def set_session():
    session['username'] = request.form['username']
    print(f'Setting session username to: {session['username']}')
    return redirect(url_for('get_session'))

@app.route('/get_session')
def get_session():
    username = session.get('username', 'Guest')
    print(f'Getting session username: {username}')
    return render_template('get_session.html', message=f'Hello, {username}!')



@app.route('/logout')
def logout():
    username = session.pop('username', None)
    print(f'Logging out, removed username from session: {username}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
