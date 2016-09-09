from flask import Flask, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'im905457'
app.config['MYSQL_DATABASE_PASSWORD'] = '19860601'
app.config['MYSQL_DATABASE_DB'] = 'innodb'
app.config['MYSQL_DATABASE_HOST'] = 'aws-rds.cm1lnnlrbky4.ap-northeast-1.rds.amazonaws.com'
mysql.init_app(app)

@app.route('/')
def hello_world():
  return 'Hello from Flask!'

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/countme/<input_str>')
def count_me(input_str):
    return input_str

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