from flask import Flask, request, jsonify, render_template, url_for
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

@app.route('/')
def hello_world():
	return 'Hello from EC2 + Ubuntu Flask + git! ver 3.0'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
	if name is None:
		name = 'Guest'
	return render_template('hello.html', name=name)
	
@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/reg', methods=['POST'])
def reg():
	# read the posted values from the UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	# validate the received values
	if _name and _email and _password:
		return '登入成功!'
	else:
		return '缺少必要參數'

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

if __name__ == '__main__':
  app.run()
