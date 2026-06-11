import pymysql
#---CREATE A CONNECTION---
con=pymysql.connect(
    host='localhost',
    user='root',
    password='admin',
    db='v2tracker')
cur=con.cursor()

#---USER LOGIN---
print ("welcome")
print('''1. Login to your account
    2. create new account''')
var=int(input("enter your choice"))
def login():
    username=input("enter username")
    pwd=input("enter password")
    cur.execute("select * from user_info where username='{}'".format(username))
    for i in cur.fetchall():
        if i[2]==pwd:
            print("login successfull!")
            return i[0]
        else:
            print("username or password incorrect")
            return None
def signup():
    username=input("select a username")
    pwd=input("select a password")
    query=('''insert into user_info (username,password)
           values('{}','{}') '''.format(username,pwd))
    cur.execute(query)
    con.commit()
    print("new account successful!")
    print("continue loging in")
    login()
if var==1:
    u_id=login()
elif var==2:
    u_id=signup()
con.close()
        
        

