from flask import Flask, render_template,request, make_response,session
import pymysql as sql

app = Flask(__name__)

app.secret_key='hdgfgdhgfghfuherfbhdfbkdjvhdfhbhfkjfdh'

def db_connect():
    conn = sql.connect(host='localhost',port=3306, user='root',password='',database='flask')
    cur=conn.cursor()
    return conn,cur

@app.route('/')
def home():
    # if request.cookies.get('islogin'):
    #     return render_template('afterlogin.html')
    if session.get('islogin'):
        return render_template('afterlogin.html')
    else:
        return render_template('index.html')

@app.route('/login/')
def login():
     
    # if request.cookies.get('islogin'):
    #     return render_template('afterlogin.html')
    if session.get('islogin'):
        return render_template('afterlogin.html')

    return render_template('login.html')

@app.route('/logout/')
def logout():
    # resp=make_response(render_template('login.html'))
    # resp.delete_cookie('email')
    # resp.delete_cookie('islogin')
    # return resp
    if session.get('islogin'):
        del session['islogin']
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/afterlogin/', methods=['GET','POST'])
def afterlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn,cur=db_connect()
        cmd=f"select * from data where email='{email}' and password ='{password}'"
        data=cur.execute(cmd)
        if data: 
            msg="login successfully......"
            # resp=make_response(render_template('afterlogin.html',m=msg))
            # resp.set_cookie('email',email)
            # resp.set_cookie('islogin','True')
            # return resp
            session['email']=email
            session['islogin']='True'
            return render_template('afterlogin.html')
        else:
            msg="increct email or password please check ....."
            return render_template('login.html', m=msg)


@app.route('/signup/')
def signup():
    # if request.cookies.get('islogin'):
    #     return render_template('afterlogin.html')
    if session.get('islogin'):
        return render_template('afterlogin.html')
    return render_template('signup.html')

@app.route('/aftersignup/', methods=['GET','POST'])
def aftersignup():
    if request.method == 'POST':
        email = request.form.get('email')
        password= request.form.get('password')
        conn,cur=db_connect()
        cmd=f"select * from data where email='{email}'"
        data=cur.execute(cmd)
        if data:
            msg = "email is already exist...."
            return render_template('signup.html', m=msg)
        else:
            cmd = f"insert into data values('{email}','{password}')"
            conn,cur = db_connect()
            cur.execute(cmd)
            conn.commit()
            msg="account created sucessfully....."
            return render_template('signup.html', m=msg)

    else:
        return render_template('signup.html')
    
    
    

app.run(debug=True)