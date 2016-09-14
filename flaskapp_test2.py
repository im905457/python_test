from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.sql import select
engine = create_engine("mysql://im905457:19860601@aws-rds.cm1lnnlrbky4.ap-northeast-1.rds.amazonaws.com/innodb?charset=utf8",encoding="utf-8", echo=True)

@app.route('/')
def hello_world():
s = select([MEMBER_DATA])
result = conn.execute(s)
for row in result:
	print(row)
result.close()

if __name__ == '__main__':
  app.run(debug=True)