from flask import Flask
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
#from sqlalchemy.sql import select
app = Flask(__name__)
engine = create_engine("mysql+pymysql://im905457:19860601@aws-rds.cm1lnnlrbky4.ap-northeast-1.rds.amazonaws.com/innodb?charset=utf8",encoding="utf-8", echo=True)
conn = engine.connect()
@app.route('/')
def hello_world():
	s = select([MEMBER_DATA])
	result = conn.execute(s)
	row = result.fetchone()
	print("name:", row['MEMBER_SN'], "; fullname:", row['MEMBER_ID'])

	result.close()

if __name__ == '__main__':
	app.run(debug=True)