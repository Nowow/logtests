from flask import Flask, session, redirect, url_for, escape, request, render_template
from simplepam import authenticate

DEFAULT_PORT = 5000
ADDITIVE_FOR_UID = 1000

try:
    from os import getuid

except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
#    if 'username' in session:
#        return 'Logged in as %s' % escape(session['username'])
#    return 'You are not logged in'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(str(username), str(password)):
            session['username'] = request.form['username']
            return 'DADADA BICH'
    else:
        if 'username' in session:
            return render_template('sassy.html', item = escape(session['username']))
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(str(username), str(password)):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return 'Invalid username/password'
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(port=getuid() + ADDITIVE_FOR_UID, debug=True)
