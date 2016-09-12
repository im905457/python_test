from flask import Flask, request, jsonify, abort, make_response
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'im905457'
app.config['MYSQL_DATABASE_PASSWORD'] = '19860601'
app.config['MYSQL_DATABASE_DB'] = 'innodb'
app.config['MYSQL_DATABASE_HOST'] = 'aws-rds.cm1lnnlrbky4.ap-northeast-1.rds.amazonaws.com'
mysql.init_app(app)
genres = [
    {
        'id': 1,
        'name': u'Trash Metal',
        'bands': u'Metallica, Megadeth'
    },
    {
        'id': 2,
        'name': u'Death Metal',
        'bands': u'Dark Tranquility, Inflames'
    }
]
@app.route('/')
def hello_world():
	return 'Hello from EC2 + Ubuntu Flask + git! ver 3.0'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    if name is None:
        name = 'World'
    return '<h1>Hello %s!</h1>' % name

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'This is a POST request'
    else:
        return 'This is a GET request'

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/countme/<input_str>')
def count_me(input_str):
    return input_str

#Get genres
@app.route('/api/genres', methods=['GET'])
def genres():
	return jsonify({'genres': genres})

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

#404 not found 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

#401 unauthorized access
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
	
if __name__ == '__main__':
  app.run()
