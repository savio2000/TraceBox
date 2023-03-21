from flask import Flask, render_template, url_for, request,flash,session,redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("create table if not exists customer(username text primary key,password text)")
con.close()

@app.route('/') 
def honey():
    return render_template('home.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
            # print(con)
        cur=con.cursor()
        cur.execute("select * from customer where username=? and password=?",(username,password))
        data=cur.fetchone()
        if data:
            session["username"]=data["username"].capitalize().split(" ")[0]
            session["password"]=data["password"]
            return redirect("customer")
    return render_template('login.html')   
@app.route('/customer',methods=['GET','POST'])
def customer():
    return render_template("customer1.html")
@app.route('/logout')    
def logout():
    session.clear()
    return redirect(url_for("honey"))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        try:
            username=request.form['name']
            password=request.form['password']
            con=sqlite3.connect("database.db")
            print(con)
            cur=con.cursor()
            cur.execute("insert into customer(username,password)values(?,?)",(username,password))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in insert","danger")
            return redirect(url_for("signup"))
        finally:          
            return redirect(url_for("login"))
            con.close()
    return render_template('signup.html')      
if __name__ == "__main__":
    app.run(debug=True)