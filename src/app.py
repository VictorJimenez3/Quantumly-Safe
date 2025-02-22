#packages
from flask import Flask, session, redirect, url_for, request, render_template
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash

#built-ins
from dotenv import load_dotenv
import time, threading
import os

#local files
from db import add_user, get_user

#app definition
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager(app)

#classes and helpers
class User(UserMixin):

    def __init__(self, unm: str, pw: str, ip: str, active=True):
        self.id = unm + "@" + ip
        
        self.ip = ip
        self.name = unm
        self.pw = pw
        
        self.active = active #should be true if __init__ called from login scope, maybe not for copying from DBMS

        self.activity_loop = threading.Thread(target=lambda: self.check_active)

    def is_active(self): 
        return self.active
    
    def check_active(self):
        while True:
            if self.activity_timeout_t > time.time():
                self.active = False
                #TODO store IP stats to db
                break
            time.sleep(0.01)
    
    def get_id(self):
        return self.id

    @login_manager.user_loader
    def load_user(id):
        # 1. Fetch against the database a user by `id` 
        # 2. Create a new object of `User` class and return it.
        u = get_user(id) #id is concat("username" + "@" + ip)
        return User(u.un, u.pw, u.ip, u.active)

    def is_anonymous(self): #no users will be conisdered guests on site, all must login
        return False

    def is_authenticated(self): #no defined auth metric yet, on itinerary
        return True
    
#app implementation

load_dotenv()


@app.route('/')
def index():
    return render_template('index.html')  # Render the index.html file

@socketio.on("update-activity") 
def update_activity():
    #will send periodic messages to this handler on different clients to remind DBMS and ML model that we should continue to consider
    current_user.activity_timeout_t = time.time() + 5*60 # 5-min timeout

@app.route('/api/login/', methods=['POST'])
def login():
    """
    Form elements will be replaced in future with API headers,
    password will become API-key
    """
    domain = "http://localhost" #WILL BE SENT OVER AS RESPONSE HEADER TODO API

    unm = request.form['username']
    passhash = generate_password_hash(os.environ.get("PEPPER", "") + request.form['password'])
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    login_user(User(unm, passhash, ip, user_agent, domain, active=True), remember=True) #will initialize activity timer & timeout

    return redirect(url_for('index'))

@app.route('/api/logout', methods=["POST"])
@login_required #TODO begone in case of API deployement
def logout():
    logout_user() #TODO manually stop timer and timeout
    return redirect(url_for('index'))

if __name__ == '__main__':
    login_manager.init_app(app)
    socketio.run(app, debug=True)