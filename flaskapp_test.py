from flask import Flask, session, request, jsonify, render_template, redirect, url_for
from datetime import datetime
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'im905457'
app.config['MYSQL_DATABASE_PASSWORD'] = '19860601'
app.config['MYSQL_DATABASE_DB'] = 'innodb'
app.config['MYSQL_DATABASE_HOST'] = 'aws-rds.cm1lnnlrbky4.ap-northeast-1.rds.amazonaws.com'
mysql.init_app(app)

list = [
	{'subject1': 'Math', 'val': 2},
	{'subject2': 'English', 'val': 10},
	{'names': { 'first_name': 'Chengyu', 'last_name': 'Tsai'}}, 
	{'score': 98},
	{'grade': 'A'}
]
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

def dir_func():
	return 'guestname is empty, you are directing to dir_func...'

@app.route('/')
def hello_world():
	return 'Hello from EC2 + Ubuntu Flask + git! ver 3.0'
	
@app.route('/guest')
@app.route('/guest/<name>')
def guest(name=None):
	if name is None:
		return dir_func()
	else:
		return 'Welcome, guest %s' % name

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
	if name is None:
		name = 'Guest'
	return render_template('hello.html', name=name)
	
@app.route('/signup')
def signup():
	#session.clear()
	return render_template('signup.html', session=session)

@app.route('/reg', methods=['POST'])
def reg():
	# read the posted values from the UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from MEMBER_DATA where MEMBER_ID = '" + _name + "' ")
	data = cursor.fetchone()
	# validate the received values
	if data is not None:
		#return '登入成功!'
		timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		query = "INSERT INTO MEMBER_LOGIN (MEMBER_SN, LOG_TIME) VALUES (%s, %s)", (data[0], timestamp)
		cursor.execute(query)
		mysql.connect().commit()
		return query
		#session.clear()
		#return redirect(url_for('.getUserAgent'))
	elif _name and _email and _password:
		#return '帳號不存在!'
		session['error'] = '帳號不存在!'
		return redirect(url_for('.signup'))
	else:
		#return '缺少必要參數'
		session['error'] = '缺少必要參數!'
		return redirect(url_for('.signup'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'This is a POST request'
    else:
        return 'This is a GET request'

@app.route('/countme/<input_str>')
def count_me(input_str):
    return input_str

@app.route('/genres')
def genres():
	return jsonify(genres_data=list)

@app.route("/auth/<msn>")
def auth(msn):
    mid = request.args.get('UserName')
    #pwd = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from MEMBER_DATA where MEMBER_SN = '" + msn +"' AND MEMBER_ID = '" + mid + "' ")
    data = cursor.fetchone()
    if data is None:
        return 'no data!'
    else:
        return "USER NAME: %s" % data[3]

@app.route('/getUserAgent')
def getUserAgent():
	userAgentString = request.headers.get('User-Agent')
	user_agent = request.user_agent
	ip = request.remote_addr
	return render_template('UserAgent.html', userAgentString=userAgentString, user_agent=user_agent, user_ip=ip, timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
  app.run()