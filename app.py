from flask import Flask, flash, render_template, request, url_for, redirect, make_response,session,abort, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
import os.path
import random
import hashlib

# Upload folder for pictures and extensions
UPLOAD_FOLDER = "static/pictures"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png"])
PASSWORD_HASH = "pgWTs7h25g8L5BH"

# Flask app with upload folder
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MONGO_URI"] = "mongodb://localhost:27017/hw-2"
# Secret key for flash messages
app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'

# Mongodb client
mongo = PyMongo()

# Mongodb collections
mongo.init_app(app)
users = mongo.db.users

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=('GET', 'POST'))
def index():
    user_in_session = 'username' in session  
    if user_in_session:
        # flash('Logged back in successfully', 'other')
        return redirect(url_for('profile'))

    if request.method=='POST':
        username = request.form["username_l"]
        password = request.form["password_l"]
        if not username:
            flash('You have not provided a username', 'danger')
        elif not password:
            flash('You have not provided a password', 'danger')
        else:
            user_exists = users.find_one({'username': username})
            if not user_exists:
                flash('Wrong login or password', 'danger')
                return redirect(url_for('index'))
            if check_password_hash(user_exists['password'], password) == False:
                flash('Wrong login or password', 'danger')
                return redirect(url_for('index'))
            
            flash('Logged in successfully.', 'success')
            resp = make_response(redirect(url_for('profile')))
            session['username'] = username
            return resp

    return render_template('index.html', stylesheet="/static/css/style.css") # @TODO Change path to dynamic



@app.route('/signup', methods=('GET', 'POST'))
def signup():
    user_in_session = 'username' in session  
    if user_in_session:
        # flash('Logged back in successfully', 'success')
        return redirect(url_for('profile'))

    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]

        fullname = request.form["fullname"]
        designation = request.form["designation"]
        if not username:
            flash('You have not provided a username', 'danger')
        elif not password:
            flash('You have not provided a password', 'danger')
        else:
            same_username = users.find_one({'username': username})
            if same_username:
                flash('This username is already taken, please choose another one', 'danger')
                return redirect(url_for('signup'))
            
            encrypted_password = generate_password_hash(password)
            users.insert_one(
                {'username': username, 'password': encrypted_password,
                    'designation':designation, 'fullname':fullname, 'avatar_url': '/static/missing-avatar.png' })
            
            flash('New User created successfully.', 'success')
            resp = make_response(redirect(url_for('profile')))
            session['username'] = username
            return resp

    return render_template('signup.html')


@app.route('/profile', methods=('GET', 'POST'))
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))

    user_session = session['username']
    if not user_session:
        flash('Session expired. Please reconnect.', 'danger')
        return redirect(url_for('index'))

    data = mongo.db.users.find_one(filter={"username": session['username']})
    return render_template('profile.html', name=user_session, data = data)



@app.route('/update-password', methods=('GET', 'POST'))
def update_password():
    if 'username' not in session:
        flash('Session expired. Please reconnect.', 'danger')
        return redirect(url_for('index'))

    user_session = session['username']

    if request.method == "POST":
        password = request.form["password"]
        confirmation_password = request.form["c_password"]
        if not password or not confirmation_password:
            flash("No info entered", 'danger')
        elif password != confirmation_password:
            flash("Passwords do not match", 'danger')
        else:
            query = {"username": user_session}

            hashed_password = generate_password_hash(password)
            newvalues = {"$set": {"username": user_session, "password": hashed_password}}
            users.update_one(query, newvalues)
            flash("Password was just updated", 'success')
            return redirect(url_for('index'))

    return render_template('update-password.html', name=user_session)



@app.route('/update-profile', methods=('GET', 'POST'))
def update_profile():
    if 'username' not in session:
        flash('Session expired. Please reconnect.', 'danger')
        return redirect(url_for('index'))


    user_session = session['username']

    if request.method == "POST":
        designation = request.form["designation"]
        fullname = request.form["fullname"]
        if not fullname or not fullname:
            flash("No info entered", 'danger')
        else:
            
            AVATARS_FOLDER = './static/avatars/'    
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

            query = {"username": user_session}
            if request.files.__len__() > 0:
                avatar_data = request.files['file']
                filename = f'{user_session}{os.path.splitext(avatar_data.filename)[1]}'

                folder = os.path.abspath(AVATARS_FOLDER)
                path = os.path.join(folder, filename)
                os.makedirs(folder, exist_ok=True)

                avatar_data.save(path)

                mongo.db.users.update_one({'username': session['username']}, {"$set": {
                    'avatar_url': f'/static/avatars/{filename}',
                }})

                newvalues = {"$set": {"fullname": fullname, "designation": designation,'avatar_url': f'/static/avatars/{filename}' }}
                users.update_one(query, newvalues)
            else:
                newvalues = {"$set": {"fullname": fullname, "designation": designation}}
                users.update_one(query, newvalues)

            flash("Profile was just updated", 'success')
            return redirect(url_for('index'))
        
    data = mongo.db.users.find_one(filter={"username": session['username']})
    return render_template('update-profile.html', data = data)



@app.route('/logout', methods=['POST'])
def sign_out():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
    

