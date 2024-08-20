from flask import Flask, render_template, redirect, url_for, session, request
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase Admin SDK
cred = credentials.Certificate("logingoogle.json")
firebase_admin.initialize_app(cred)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_google', methods=['POST'])
def login_google():
    id_token = request.form['id_token']
    try:
        # Verify the token with Firebase
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        session['user_id'] = user_id
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Error verifying token: {e}")
        return 'Authentication failed', 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
