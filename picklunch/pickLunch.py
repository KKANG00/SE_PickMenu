from numpy import genfromtxt
from flask import Flask, render_template, redirect,request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import csv
import pandas as pd
import random

app = Flask(__name__)

#데이터 베이스 생성
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///storedata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'other string'

db=SQLAlchemy(app)

#데이터 베이스 테이블 생성
class STORE(db.Model):
   #id=db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
   name=db.Column(db.String(100),primary_key=True, nullable=False, default='')
   number=db.Column(db.String(100), nullable=True, default='')
   address=db.Column(db.String(100), nullable=True, default='')
   category=db.Column(db.String(100), nullable=True, default='')
   choice=db.Column(db.String(100), nullable=True, default='X')
   delivery=db.Column(db.String(100), nullable=True, default='X')

   #데이터 베이스 생성자
   def __init__(self, name, address, delivery, number, category):
      self.name=name
      self.number=number
      self.address=address
      self.category=category
      self.choice='X'
      self.delivery=delivery

   def SetStore(ox):
   	  STORE_=STORE.query.all()
   	  for i in STORE_:
   	  	i.choice=ox
   	  db.session.commit()

class MANAGER():
	password = 'dnflskfk'

	def __init__(self, password):
		self.password=password

	def getpw(self):
		return self.password

#엑셀 데이터 동기화
#df = pd.read_csv('store_db.csv', encoding='CP949')
#engine = create_engine('sqlite:///storedata.db')
#df.to_sql('STORE', con=engine, if_exists='replace')

#매니저 객체
M=MANAGER('dnflskfk')


#메인화면루트
@app.route('/')
def SetUserDelivery():
	STORE.SetStore('X')
	return render_template('howToEat.html')
	#return render_template('list.html',STORELIST=STORE.query.order_by('category').all())

#<사용자 모드>

#식사방법고르기
@app.route('/<howtoeat>/howtochoose')
def SetUertChoice(howtoeat):
	if(howtoeat=='delivery'):
		return render_template('howToChoose_deli.html')
	elif(howtoeat=='goto'):
		return render_template('howToChoose_goto.html')

#선택방법고르기
@app.route('/<eat>/<choose>/<check>')
def fourcases(eat, choose, check):
	if(eat=='goto'):
		if(choose=='like'):
			if check=='reset':
				STORE.SetStore('X')
			return render_template('listgl.html', STORELIST=STORE.query.order_by('category').all())
		elif(choose=='without'):
			if check=='reset':
				STORE.SetStore('O')
			return render_template('listgw.html', STORELIST=STORE.query.order_by('category').all())
	elif(eat=='delivery'):
		if(choose=='like'):
			if check=='reset':
				STORE.SetStore('X')
			return render_template('listdl.html', STORELIST=STORE.query.order_by('category').filter_by(delivery='O').all())
		elif(choose=='without'):
			if check=='reset':
				STORE.SetStore('O')
			return render_template('listdw.html', STORELIST=STORE.query.order_by('category').filter_by(delivery='O').all())

@app.route('/choice/<deli>/<lw>/<name>')
def Select(deli, lw, name):
  des=STORE.query.get(name)
  if des.choice=='O':
     des.choice='X'
  else :
     des.choice='O'
  db.session.commit()
  return redirect('/'+deli+'/'+lw+'/pass')

@app.route('/choice')
def MakeList():
	return render_template('choice.html',CHOICE=STORE.query.filter_by(choice='O').order_by('category').all())

@app.route('/result/<count>')
def PickRandomStore(count):
    count = int(count)
    if(count<=3):
        CHOICE = STORE.query.filter_by(choice='O').all()
        lenth = len(CHOICE)
        ran = random.randrange(1,lenth)
        result_choice = CHOICE[ran]
        result_choice.choice = 'X'
        db.session.commit()
    else:
        flash('No more chance to pick lunch','error')
    return render_template('result.html',result_choice = result_choice)


#<매니저 모드>

#로그인루트
@app.route('/login', methods=['GET', 'POST'])
def Login():
	if request.method == 'POST':
		if not request.form['password']:
			flash('Please enter password', 'error')
			return redirect("/")
		if M.getpw()==request.form['password']:
			return redirect("/manager")
		return redirect("/")

@app.route('/manager')
def ShowInfo():
	return render_template('manage_list.html', STORELIST=STORE.query.order_by('category').all())

@app.route('/new', methods=['GET', 'POST'])
def AddInfo():
    if request.method == 'POST':
       #빈칸 입력시 추가되지 않음
       if not request.form['name']:
          flash('Please enter all the fields', 'error')
       else:
          #입력받은 정보를 받아와서 연락처 추가
          NEW=STORE(request.form['name'],request.form['address'],request.form['delivery'],request.form['number'],request.form['category'])
          db.session.add(NEW)
          db.session.commit()
       return redirect('/manager')

@app.route('/delete/<name>')
def DeleteInfo(name):
	deleted=STORE.query.filter_by(name=name)
	deleted.delete()
	db.session.commit()
	return redirect('/manager')

@app.route('/edit/<name>', methods=['POST'])
def ChangeInfo(name):
   edited=STORE.query.get(name)
   edited.name=request.form['name']
   edited.number=request.form['number']
   edited.email=request.form['delivery']
   edited.email=request.form['address']
   edited.email=request.form['category']
   db.session.commit()
   return redirect('/manager')


if __name__ == '__main__' :
   db.create_all()
   app.run(debug=True)
