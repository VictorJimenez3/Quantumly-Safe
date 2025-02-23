#packages
from flask import Flask, redirect, url_for, request, jsonify
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from flask_socketio import SocketIO
from flask_cors import CORS

from werkzeug.security import generate_password_hash, check_password_hash

#built-ins
from dotenv import load_dotenv
import time, threading, json
import os

#local files
from db import DB
quantum_random_forest = lambda data: None 

#app definition
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "")
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager(app)

db = DB()

def aggregate_and_format_for_qrf(data: dict):
    """
    TODO define integration that aggregates previous user variables (if exists) in db
    to those defined in data, grab activities data from activities bucket.

    Compile into format for quantum random forest
    """

    return None

#classes and helpers
class User(UserMixin):

    def __init__(self, data: dict):
        """
        data:
        {
            "ip" : client_ip,
            "user_agent" : ip of website,
            "username" : username,
            "password" : hashed (client side & salt & peppered) password
            ...
        }
        """

        self.id = data["ip"] + "@" + data["userAgent"]
        self.username = data.get("username", None)
        self.password = data.get("password", None)
        
        self.data = data
        
        self.active = True #should be true if __init__ called from login scope, maybe not for copying from DBMS

    def is_active(self): 
        return True
        
    def get_id(self):
        return self.id

    @login_manager.user_loader
    def load_user(uuid):

        user_data = db.get_user(uuid)

        return User(data = user_data)

    def is_anonymous(self): #no users will be conisdered guests on site, all must login
        return False

    def is_authenticated(self): #no defined auth metric yet, on itinerary
        return True
    
#app implementation
load_dotenv()

@app.route('/')
def visualization():
    return redirect("http://www.quantumlysafe.tech/") #TODO change to streamlit location

@app.route("/api/validate_user")
def _1():
    form = lambda x: jsonify({"flag" : x})
    body = request.data

    try:
        data = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"ERR, cannot cast request body to JSON entity: {e}")

    u = db.get_users_by_username(domain = data["domainName"], username = data["username"])
    
    if u is not None and len(u):
        if(check_password_hash(u[0]["password"], data['password'])):
            return form(1)
        return form(0)
    else:
        return form(-1)

@app.route("/api/send_preliminary_data", methods=['POST']) #DATA AQUISITION DONE
def _2():
    body = request.data

    try:
        data = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"ERR, cannot cast request body to JSON entity: {e}")

    ip = data.get("ip", None)
    domainName = data.get("domainName", None)
    userAgent = data.get("userAgent", None)

    return jsonify({"status" : 200})

@app.route('/api/login', methods=['POST'])
def _3():
    body = request.data
    
    try:
        data = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"ERR, cannot cast request body to JSON entity: {e}")

    # Check if the user exists in the database
    print(data["domainName"], data["username"])
    u = db.get_users_by_username(data["domainName"], data["username"])  # Uncomment and implement this line to fetch user from DB

    print("USERS EXISTING FOR SIGN-IN", u)

    if u is None or not len(u):
        return jsonify({"status": 404, "message": "User not found"})

    u = u[0] #we assume only one user pops up (hopefully!!)

    # # Verify the password
    if not u["password"] == data['password']:
        return jsonify({"status": 401, "message": "Invalid password"}), 401

    login_user(User(u), remember=True)

    print(data)

    db.aggregate_user_signin(data["ip"], data["domain"], data["username"], data["failedAttempts"], data["totalAttempts"])

    example = db.get_users_by_username(data["domain"], data["username"])[0]
    print(example)
    
    return jsonify({
        "status" : 200,
        "is-attacking": quantum_random_forest(aggregate_and_format_for_qrf(current_user))
    })

@app.route('/api/signup', methods=['POST'])
def _4():
    body = request.data

    try:
        data = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"ERR, cannot cast request body to JSON entity: {e}")
    
    print(data)
    print(data["domainName"], data["username"])
    u = db.get_users_by_username(data["domainName"], data["username"]) 

    print("USERS EXISTING FOR SIGN-UP: ", u)

    if (u is not None and type(u) != list) or len(u):
        return jsonify({"status": 401, "message": f"User {data['username']} exists already"})

    user = User(data)

    login_user(user, remember=True)

    db.add_interactions(data) #make user, no aggregation needed

    return jsonify({
        "status" : 200,
        "is-attacking": quantum_random_forest(aggregate_and_format_for_qrf(current_user))
    })

if __name__ == '__main__':
    login_manager.init_app(app)
    socketio.run(app, host="0.0.0.0", debug=True)