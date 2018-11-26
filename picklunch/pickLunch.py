from numpy import genfromtxt
from flask import Flask, render_template, redirect,request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import csv
import pandas as pd


app = Flask(__name__)

#데이터 베이스 생성
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///storedata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = "other string"

db=SQLAlchemy(app)

#데이터 베이스 테이블 생성
class STORE(db.Model):
   #id=db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
   name=db.Column(db.String(100),primary_key=True, nullable=False, default='')
   number=db.Column(db.String(100), nullable=True, default='')
   address=db.Column(db.String(100), nullable=True, default='')
   category=db.Column(db.String(100), nullable=True, default='')
   choice=db.Column(db.Boolean, default=False)
   delivery=db.Column(db.Boolean, default=False)



   #데이터 베이스 생성자
   def __init__(self, name, address, delivery, number, category):
      self.name=name
      self.number=number
      self.address=address
      self.category=category
      self.choice=False
      if delivery=='O':
       self.delivery=True
      else:
         self.delivery=False


#db 업데이트되는 경우에만..? 음 엥 모르겟다
df = pd.read_csv('store_db.csv', encoding='CP949')
engine = create_engine('sqlite:///storedata.db')
df.to_sql('STORE', con=engine, if_exists='replace')


#메인화면루트
@app.route("/")
def main():
   return render_template('main.html', STORElist=STORE.query.order_by("category").all())

#추가화면 루트
@app.route("/new", methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
       #빈칸 입력시 추가되지 않음
       if not request.form['name']:
          flash('Please enter all the fields', 'error')
       else:
          #입력받은 정보를 받아와서 연락처 추가
          NEW=STORE(request.form['name'],request.form['address'],request.form['delivery'],request.form['number'],request.form['category'])
          db.session.add(NEW)
          db.session.commit()
       return redirect("/")

if __name__ == "__main__" :
   db.create_all()
   app.run(debug=True)
