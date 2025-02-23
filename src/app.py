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
# from db import add_user, get_user
quantum_random_forest = lambda data: None 

#app definition
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "")
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager(app)

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
            "userAgent" : ip of website,
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
    def load_user(id):
        # u = get_user(id) #id is concat("username" + "@" + ip) TODO
        u = {
            "ip": "192.168.1.1",
            "domain": "example.com",
            "username": "sample_user",
            "email": "sample_user@example.com",
            "last_login": time.time(),
            "activities": []  # This can be populated with activity data if needed
        }

        u["id"] = f"{u['ip']}@{u['domain']}"
        return User(u.data)

    def is_anonymous(self): #no users will be conisdered guests on site, all must login
        return False

    def is_authenticated(self): #no defined auth metric yet, on itinerary
        return True
    
#app implementation
load_dotenv()

@app.route('/')
def visualization():
    return redirect("https://walmart.com") #TODO change to streamlit location

@app.route("/api/validate_user")
def _1():
    form = lambda x: jsonify({"flag" : x})
    body = request.data

    # u = get_user(body["username"])

    # if u is not None:
        # if(check_password_hash(u["hashed_password"], body['password'])):
            # return form(1)
        # return form(0)
    # else:
        # return form(-1)

    form(1)

@app.route("/api/send_preliminary_data", methods=['POST']) #DATA AQUISITION DONE
def _2():
    body = request.data
    print("prelinimnary_data: ",body)

    #TODO grab variables, store

    return jsonify({"status" : 200})

@app.route('/api/login', methods=['POST'])
def _3():
    body = request.data
    # print("login data: ",body)
    try:
        data = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"ERR, cannot cast request body to JSON entity: {e}")

    # Check if the user exists in the database
    # u = get_user(body["username"])  # Uncomment and implement this line to fetch user from DB
    # u = None  # Placeholder for user fetching logic

    # if u is None:
    #     return jsonify({"status": 404, "message": "User not found"}), 404

    # # Verify the password
    # if not check_password_hash(u["hashed_password"], request.form['password']):
    #     return jsonify({"status": 401, "message": "Invalid password"}), 401

    # login_user(u, remember=True)

    print(data)

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

    # u = get_user(body["username"])  # Uncomment and implement this line to fetch user from DB

    # if u is not None:
    #     return jsonify({"status": 401, "message": f"User {data['username']} exists already"}), 404

    # # Verify the password
    # if not check_password_hash(u["hashed_password"], ['password']):
    #     return jsonify({"status": 401, "message": "Invalid password"}), 401

    # user = User(body) #make user

    # login_user(user, remember=True)

    # set_user(body)

    return jsonify({
        "status" : 200,
        "is-attacking": quantum_random_forest(aggregate_and_format_for_qrf(current_user))
    })

if __name__ == '__main__':
    login_manager.init_app(app)
    socketio.run(app, host="0.0.0.0", debug=True)