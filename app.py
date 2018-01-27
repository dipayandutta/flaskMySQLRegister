'''
	pip install flask-mysqldb
	pip install FlaskWTF
	pip install passlib
'''
from flask import Flask , render_template,request
from data import Articles 
from flask import flash, redirect , url_for ,session,logging
from flask_mysqldb import MySQL 
from wtforms import Form,StringField,TextAreaField,PasswordField,validators #This is form form creation and validation
from passlib.hash import sha256_crypt #import this which will encrypt the password

app = Flask(__name__)


#MySQL Configurations 
app.config['MYSQL_HOST'] 		= 'localhost'
app.config['MYSQL_USER'] 		= 'root'
app.config['MYSQL_PASSWORD']	= 'node'
app.config['MYSQL_DB']			= 'myflaskapp'
# CURSORCLASS is kind of a helper
# Here i want to return the result as key,value pair i.e. a Python Dictonary
app.config['MYSQL_CURSORCLASS']	= 'DictCursor'			


#Initializing MySQL

mysql = MySQL(app) #Using this we can create the cursor and make quaries

#Making debug True For Development Purpose
#Make this False in Production
app.debug=True

#Getting the Articles Values from the data.py file
Articles = Articles()

@app.route('/')

def index():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/article')
def articles():
	return render_template('articles.html',articles=Articles)

@app.route('/articles/<string:id>')
def article(id):
	return render_template('article.html',id=id)


#Creating the Form Class 
#For WTF form make in action we have to create a class and pass Form

class RegisterForm(Form):
	name 		= StringField('Name',[validators.Length(min=1,max=50)])# Name Field with max and min length
	username	= StringField('User Name',[validators.Length(min=5,max=20)]) #username Field with max and min length
	email		= StringField('Email',[validators.Length(min=6,max=40)]) # Email field with max and min lenght
	#Creating The password field which will be Equal to another field name confirm
	password 	= PasswordField('Password',[
				  validators.DataRequired(),
				  validators.EqualTo('confirm',message='Password Dont Match')
		])
	#Creating the Confirm field for password Matching
	confirm		= PasswordField('confirm Password')


#Creating the Route for the Registration for 
# Both POST and GET used
@app.route('/register',methods=['GET','POST'])
#The register URL Function defination 
def register():
	form = RegisterForm(request.form) # calling the RegisterForm class

	#Checking if the Form method is POST and also it is validated
	if request.method == 'POST' and form.validate():
		# code for form value data base submission
		#First Getting the Form Values

		name 		= form.name.data 
		email 		= form.email.data
		username 	= form.username.data 
		password 	= sha256_crypt.encrypt(str(form.password.data)) #Wrap the password in encrption wrapper


		# Create the Cursor 
		cur = mysql.connection.cursor()

		#Excute Commands using the connected Cursor
		cur.execute("INSERT INTO users(name,email,username,password) VALUES (%s , %s , %s , %s)",(name,email,username,password)) 

		#Commit To Database
		mysql.connection.commit()

		#Close the Connection 
		cur.close()

		#Set the Flash Message after registered

		flash('You are Registered ','success') # For setting the Flash messages with catagories , we have to add a templapte and also add the template in the layout.html file
		
		#Redirecting in the Index Page after successful Registration
		return redirect(url_for('index'))


	return render_template('register.html',form = form)

if __name__ == '__main__':
	app.secret_key = 'secret123'
	app.run(host='0.0.0.0',port=5000)
