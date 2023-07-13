from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/dan')
def dan():
   return 'Hello dan'

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

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
#    app.run()
    app.run('127.0.0.1', 3000, True)