from flask import *

import pymysql




app = Flask(__name__ ,template_folder='template')
app.secret_key = '@#$%5^^77*88***8'
conn = pymysql.connect(host ='localhost',user ='root',password ='', database='rentals')
cursor = conn.cursor()

@app.route('/home/') 
def home():
   return render_template("home.html")
    
  
   
 


@app.route('/signup/',methods= ['GET','POST'])
def signup():
  
  if request.method == 'POST':
    houseid =request.form['houseid']
    names = request.form['names']
    email = request .form['email']
    password = request.form['password']
    phone = request.form['phone']  
    gender = request.form['gender']
    

    if len(password) <8:
      return render_template('signup.html' , error = 'password must be 8 characters')
    else:
      conn = pymysql.connect(host ='localhost',user ='root',password ='', database='rentals')
      cursor = conn.cursor()
      cursor.execute('insert into user(houseid,names,email,password,phone,gender) values(%s,%s,%s,%s,%s,%s)',(houseid,names,email,password,phone,gender))

      conn.commit()
      return render_template('login.html' , msg ="saved succesfully")
  else :
    return render_template('signup.html')
  
  
  

@app.route('/login', methods = ['GET', 'POST'])
def login():
  if request.method =='POST':
   
    conn = pymysql.connect(host ='localhost',user ='root',password ='', database='rentals')
    cursor = conn.cursor()
    houseid = request.form['houseid']
    phone = request.form['phone']
    password  = request.form['password']
    cursor.execute('select * from user where houseid = %s and phone = %s and password = %s',(houseid,phone,password))

    if cursor.rowcount == 0:
      return render_template('login.html', error = 'wrong credentials')
    else:
      
      session['key'] = houseid
      return redirect(url_for('tenant', houseid=houseid))
    
  else:
    return render_template('login.html')
  

@app.route('/view')
def viewbooking():
    conn=pymysql.connect(host='localhost',user='root',password='',database='rentals')
    cursor=conn.cursor()
    sql='select * from  user'
    cursor.execute(sql)
    if cursor.rowcount ==0:
        return render_template('view.html',msg='No BOOKINGS AVAILABLE')
    else:
        rows= cursor.fetchall()
        return render_template('view.html', rows=rows)
    

@app.route('/tenant/<houseid>')
def tenant(houseid):
            connection = pymysql.connect(host='localhost', user='root', password='',
                                         database='rentals')

      
            cursor = connection.cursor()
       
            cursor.execute('SELECT * FROM user WHERE houseid= %s ', (houseid))
         
            row = cursor.fetchone()

            
            return render_template('tenant.html', row=row)





import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
@app.route('/mpesa',methods = ['POST','GET'])
def mpesa():
   if request.method == 'POST':
      phone = str(request.form['phone'])
      amount = str(request.form['amount'])
      consumer_key = "Apppxo6uDrve8ANzmgQ9aGSmMPF33YidB1tGbrsvzbrsHoYo"
      consumer_secret ="vGMUzXi5xFk3QGFvbq8J80BBgZef3Q9wv9wMelCGoid2LeVJ8yPW1cz655bcze8G"
      api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
      r = requests.get(api_URL, auth = HTTPBasicAuth(consumer_key,consumer_secret))

      data = r.json()

      access_token = "Bearer " + data['access_token']


      timestamp =  datetime.datetime.today().strftime('%Y%m%d%H%M%S')
      passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
      business_short_code = '174379'
      data =business_short_code + passkey +timestamp
      encoded = base64.b64encode(data.encode())
      password = encoded.decode('utf-8')

      payload = {
          
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwMzAxMTQ1MDIz",
    "Timestamp": "20240301145023",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254799604144,
    "PartyB": 174379,
    "PhoneNumber": 254799604144,
    "CallBackURL": "https://webhook.site/2efd7dd2-3e7b-4cb3-9ca2-54f1f76b63ca",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 

      }

      headers = {
         "Authorization" :access_token,
         "Content-Type" : "application/json"
      }
      url ="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
      response = requests.post(url, json= payload,headers = headers)
      print(response.text)
      return('please complete payment in your phone')
   else:
      return render_template('tenant.html')
  

      





  
 

 
 
  
  


  




if  __name__=='__main__':

  app.run(debug=True)  

