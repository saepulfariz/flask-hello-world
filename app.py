from flask import Flask, redirect, url_for, render_template, request, make_response, session,abort, flash, jsonify
from werkzeug.utils import secure_filename
import sqlite3 as sql
import pyodbc

cnxn_str = ("DRIVER={SQL Server};SERVER=172.21.202.142;DATABASE=PCS;UID=Traceability;PWD=ability")

cnxn = pyodbc.connect(cnxn_str, autocommit=True)
crsr = cnxn.cursor()
cursor = cnxn.cursor()

app = Flask(__name__)

# import events
import os
from dotenv import load_dotenv
load_dotenv()
app.secret_key = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/upload'

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# os.urandom(64)


# json out
@app.route('/json')
def send_json():
    data = {
        'name': 'John',
        'age': 30,
        'city': 'New York'
    }
    return jsonify(data)

# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
   # defining function
   return render_template("template/error/404.html")

# jika route gak bisa GET
@app.errorhandler(405)
def url_not(e):
   # defining function
   return render_template("template/error/404.html")

# get env
# print (os.environ.get('FLASK_RUN_PORT'))

# @app.route('/')
# def hello_world():
#    return 'Hello World'

@app.route("/saepulfariz")
def saepulfariz():
   return render_template("saepulfariz/index.html")

@app.route('/events',methods = ['GET'])
def events():
   
   # crsr.execute("PRINT 'Hello world!'")
   # print(crsr.messages)

   # cursor.execute("select a from tbl where b=? and c=?", (x, y))
   # data = crsr.execute("SELECT TOP(100) MCH_CODE FROM DC_EVENTS");
   # print(data)

   cursor.execute("SELECT TOP 1000 * FROM dbo.DC_EVENTS WHERE PP_CODE ='B02' AND EV_CODE='PROD' AND EV_SUBCODE='MACH'")
   data = cursor.fetchall()
   return render_template("events/index.html",data = data)

@app.route('/events/ajax_table',methods = ['GET'])
def events_ajax_table():
   cursor.execute("SELECT TOP 1000 * FROM dbo.DC_EVENTS WHERE PP_CODE ='B02' AND EV_CODE='PROD' AND EV_SUBCODE='MACH'")
   res = cursor.fetchall()
   res = [tuple(row) for row in res]
   print(res)
   data = {
      'data' : res
   }
   return jsonify(data)


@app.route("/")
def index():
   return render_template("index.html")
   
# def index():
#    if 'username' in session:
#       username = session['username']
#       return 'Logged in as ' + username + '<br>' + \
#          "<b><a href = '/logout'>click here to log out</a></b>"
#    else:
#       return "You are not logged in <br><a href = '/login'></b>" + \
#       "click here to log in</b></a>"

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/auth',methods = ['GET'])
def auth():
   return render_template("login.html")

@app.route('/login',methods = ['POST', 'GET'])
def login():
   error = None

   if request.method == 'POST':
      # user = request.form['nm']
      # return redirect(url_for('success',name = user))
      username = request.form['username']
      if request.form['username'] == 'admin' or \
         request.form['password'] == 'admin':
         alert = { 
            'icon' :'success',
            'title' :'Success',
            'text' :'Oke login',
         }
         flash(alert)
         flash('You were successfully logged in')
         flash('Oke sukses')
         session['username'] = username
         return redirect(url_for('index'))
      # if username == 'admin' :
      #    session['username'] = username
      #    return redirect('/')
         # return redirect(url_for('success'))
      else:
         # The Code parameter takes one of following values −
         # 400 − for Bad Request
         # 401 − for Unauthenticated
         # 403 − for Forbidden
         # 404 − for Not Found
         # 406 − for Not Acceptable
         # 415 − for Unsupported Media Type
         # 429 − Too Many Requests

         # HTTP_300_MULTIPLE_CHOICES
         # HTTP_301_MOVED_PERMANENTLY
         # HTTP_302_FOUND
         # HTTP_303_SEE_OTHER
         # HTTP_304_NOT_MODIFIED
         # HTTP_305_USE_PROXY
         # HTTP_306_RESERVED
         # HTTP_307_TEMPORARY_REDIRECT
         error = 'Invalid username or password. Please try again!'
         # abort(401)
   
   return render_template('login.html', error = error)
      # return render_template("login.html")
      # user = request.args.get('nm')
      # return redirect(url_for('success',name = user))

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

# FROM REQUEST
@app.route('/student')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

# upload file
@app.route('/upload')
def upload_file():
   return render_template('upload.html')

def allowed_file(filename):
   return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/uploader', methods = ['GET', 'POST'])
def proses_upload_file():
   if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
         flash('No file part')
         return redirect(request.url)
      file = request.files['file']
      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
         flash('No selected file')
         return redirect('/upload')
      if file and allowed_file(file.filename):
         # file = request.files['file']
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         return 'file uploaded successfully'
      else:
         flash('Not Allow check type upload')
         return redirect('/upload')

# COOKIE
@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
      user = request.form['nm']
      
      resp = make_response(render_template('readcookie.html'))
      resp.set_cookie('userID', user)
      return resp
      if resp :
         return redirect('/getcookie')

      # return redirect('/you_were_redirected')
      # return redirect(url_for('getcookie'))
   else : 
      return render_template('setcookie.html')


@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome '+name+'</h1>'

#SQL
@app.route('/student/new')
def new_student():
   return render_template('student/new.html')

@app.route('/student/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("student/result.html",msg = msg)
         con.close()

@app.route('/student/list')
def student_list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   return render_template("student/list.html",rows = rows)

@app.route('/dan')
def dan():
   return 'Hello dan'

# @app.route('/hello/<name>')
# def hello_name(name):
#    return 'Hello %s!' % name

# template
@app.route('/hello/<user>')
def hello_name(user):
   score = 70
   return render_template('hello.html', name = user, marks = score)

# @app.route('/result')
# def result():
#    dict = {'phy':50,'che':60,'maths':70}
#    return render_template('result.html', result = dict)



#URL 

@app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID

@app.route('/rev/<float:revNo>')
def revision(revNo):
   return 'Revision Number %f' % revNo

@app.route('/flask')
def hello_flask():
   return 'Hello Flask'

@app.route('/python/')
def hello_python():
   return 'Hello Python'


# 
@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
    # jika admin maka redirect ke function hello_admin 
      return redirect(url_for('hello_admin'))
   else:
    # jika lain maka redirect ke function hello_guest dengan parameter guest nya
      return redirect(url_for('hello_guest',guest = name))

   
# @app.route('/hello')
# def hello_world():
#    return 'hello aku'

def hay():
   return 'hello world'
app.add_url_rule('/', 'hello', hay)

if __name__ == '__main__':
   #  app.run()
   #  app.run('127.0.0.1', 3000, True)
   app.run(debug = True)