import sqlite3
import time
import os
import csv
from flask import Flask, request, session, g, redirect, url_for \
        , render_template, flash, jsonify
from werkzeug import check_password_hash, generate_password_hash, \
        secure_filename
from contextlib import closing

DATABASE = 'sample_repo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'srtest'
PASSWORD = 'pwd2012'
ALLOWED_EXTENSIONS = set(['csv', 'txt', 'CSV'])
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('IRB_DB_SETTINGS', silent = True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def connect_db():
    """Returns a new connection to the database"""
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_user_id(username):
    rv = g.db.execute('SELECT user_id FROM user where username = ?',
                        [username]).fetchone()
    return rv[0] if rv else None

def query_db(query, args=(), one = False):
    """Queries the database and returns a list of dictionaries"""
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_ids(filename):
    ids = []
    reader = csv.reader(open(filename))
    for line in reader:
        ids.append(line[0])
    return tuple(sorted(ids))


#then add some decorators

@app.before_request
def before_request():
    g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        g.user = query_db('SELECT * FROM user where user_id = ?',
                            [session['user_id']], one = True)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid password"
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return render_template('index.html')
    return render_template('login.html', error = error)

@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/all_samples', methods = ['GET', 'POST'])
def all_samples():
	error = None
	entries = query_db("""SELECT irs_id, proj_id, proj_tube_no,
                        proj_cell, date_moved, location
                        FROM sample_location""", one = False )
	return render_template('all_samples.html', entries = entries)

@app.route('/all_patients', methods = ['GET', 'POST'])
def pt_demo():
    entries = query_db("""SELECT irs_id, ptdon, sample_res, sample_type,
                            sourcecoll, sample_acc, coldate, pt_name, txdate,
                            donor_names, signed9 FROM demo""", one = False)
    return render_template('all_patients.html', entries = entries)

@app.route('/<irs_id>', methods = ['GET', 'POST'])
def indiv_results(irs_id):
    ids = str(irs_id)
    entries = query_db("""SELECT demo.irs_id, ptdon, sample_res, sample_type,
                            sourcecoll, sample_acc, coldate, pt_name, txdate,
                            donor_names, signed9, proj_id, proj_tube_no,
                            proj_cell, date_out, shipped_to, sent_to,
                            received_date FROM demo, sample_movement where
                            demo.irs_id = sample_movement.irs_id and
                            demo.irs_id = ?""", [ids])
    return render_template('get_results.html', entries = entries)

#@app.route('/receive_samples')
#def receive_samples():
#    sample_id = request.form['sample_number']
#    entries = query_db("""SELECT sample_info FROM base""", where id == 

@app.route('/query')
def query():
    return render_template('subj_query.html')

@app.route('/results', methods = ['GET', 'POST'])
def results():
    ids = str(request.form['irs_id'])
    entries = query_db("""SELECT demo.irs_id, ptdon, sample_res, sample_type,
                            sourcecoll, sample_acc, coldate, pt_name, txdate,
                            donor_names, signed9, proj_id, proj_tube_no,
                            proj_cell, date_out, shipped_to, sent_to,
                            received_date FROM demo, sample_movement where
                            demo.irs_id = sample_movement.irs_id and
                            demo.irs_id = ?""", [ids])
    return render_template('get_results.html', entries = entries)

@app.route('/create_project', methods = ['GET', 'POST'])
def create_project():
            return render_template('create_project.html')

@app.route('/send_samples', methods = ['GET', 'POST'])
def send_samples():
            return render_template('create_project.html')

@app.route('/submit_send', methods = ['GET', 'POST'])
def submit_send():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            indivs = get_ids(os.path.join(app.config['UPLOAD_FOLDER'],
                filename))
            print os.path.join(app.config['UPLOAD_FOLDER'],filename)
            print request.form['sent_to']
            entries = query_db("""SELECT * FROM sample_movement WHERE irs_id IN
                    (%s)""" % ','.join('?'*len(indivs)), indivs)
            return render_template('send_samples.html', entries=entries)

    return render_template('index.html')

#test for facebook-style timeline

@app.route('/ship_samples', methods = ['GET', 'POST'])
def ship_samples():
    pass

@app.route('/test_movement', methods = ['GET', 'POST'])
def test_movement():
	error = None
	entries = query_db("""SELECT irs_id, max(datestamp),
                        sent_from, datestamp, site FROM test_movement GROUP BY irs_id""", one = False ) 
	return render_template('test_movement.html', entries = entries)

@app.route('/movement/<irs_id>', methods = ['GET', 'POST'])
def test_indiv_results(irs_id):
    ids = str(irs_id)
    entries = query_db("""SELECT irs_id, datestamp, sent_from, site
                            FROM test_movement where irs_id = ?""", [ids])
    return render_template('indiv_sample_timeline.html', entries = entries)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))	


if __name__ == '__main__':
    app.run()
