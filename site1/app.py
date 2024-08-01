from flask import Flask, render_template, redirect, request, session, url_for
import os
# import logging

user = os.getenv('USERNAME')
passw = os.getenv('PASSWORD')
flag = os.getenv('FLAG')

new_credentials = []


app = Flask(__name__)
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app.secret_key = 'secret_key'

@app.route('/')
def index():
    global new_credentials

    # app.logger.info(new_credentials)

    if 'username' not in session:
        return render_template('login.html', invalid_credentials=False)
    else:
        usernames_given = [cred[0] for cred in new_credentials if cred]
        if session['username'] in usernames_given:
            session.pop('username', None)

        return render_template('flag.html', flag=flag)
    
@app.route('/login', methods=['POST'])
def login():
    global user, passw, new_credentials

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user == username and passw == password:
            session['username'] = username
            return redirect(url_for('index'))

        elif len(new_credentials) > 0:
            for credential in new_credentials:
                if credential[0] == username and credential[1] == password:
                    session['username'] = username
                    return redirect(url_for('index'))
    
        else:
            return render_template('login.html', invalid_credentials=True)
        
@app.route('/change_credentials', methods=['POST'])
def change_credentials():
    global new_credentials

    if request.method == 'POST':
        if 'username' in session: 
            new_username = request.form['username']
            new_password = request.form['password']

            new_credentials.append([new_username, new_password])
            
            #Thks Stack Overflow
            new_credentials = [list(t) for t in {tuple(inner_list) for inner_list in new_credentials}]
            
            # app.logger.info(new_credentials)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)