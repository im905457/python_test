from flask import Flask
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import text

app = Flask(__name__)
engine = create_engine("mysql+pymysql://im905457:19860601@aws-rds.cm1lnnlrbky4.ap-northeast-1.rds.amazonaws.com:3306/innodb?charset=utf8",encoding="utf-8", echo=True)
#engine_is = create_engine("mysql+pymysql://im905457:19860601@aws-rds.cm1lnnlrbky4.ap-northeast-1.rds.amazonaws.com:3306/information_schema?charset=utf8",encoding="utf-8", echo=True)

@app.route('/')
def hello_world():
	conn = engine.connect()
	s = text("SELECT * FROM MEMBER_DATA WHERE MEMBER_SN = :id")
	result = conn.connect(s, id='0000000001')
	row = result.fetchone()
	#print("name:", row['MEMBER_SN'], "; fullname:", row['MEMBER_ID'])
	return row['MEMBER_ID']

	result.close()

if __name__ == '__main__':
	app.run(debug=True)