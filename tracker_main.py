import pymysql
import time
import datetime
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

#----FUNCTION TO TRACK EXAMS----
#----add a new exam----
def edit_exam():
    def add_exam():
        ex_name=input('enter the name of your upcoming exam')
        ex_date=input("enter date of your upcoming exam (YYYY-MM-DD)")
        cur.execute("insert into exam_info (user_id,exam_name,exam_date) values({},'{}','{}')".format(u_id,ex_name,ex_date))
        con.commit()
        print("Exam added succesfully!")
    while True:
            edit_pref=int(input("do you wish to \n"
                                "1: add a new exam \n"
                                "2: exit\n"))
            if (edit_pref==1):
                      add_exam()
            elif(edit_pref==2):
                break
            else:
                print("invalid input!")    
#----FUNCTION TO DISPLAY LIST OF EXAMS----
def exam_list():
    cur.execute('select * from exam_info')
    rows=cur.fetchall()
    for i in rows:
        print(i)
        
#----FUNCTION TO CALCULATE DAYS REMAINING TILL EXAM----
def day_till_ex():
    cur.execute('select * from exam_info')
    for i in cur.fetchall():
        print(i)
    no=input("enter exam name\n")
    cur.execute("select * from exam_info where exam_name=(%s) and user_id=(%s)",(no,u_id))
    for i in cur.fetchall():
        name=i[2]
        date=i[3]
        time_left=(date-date.today()).days
    print(f"There are {time_left} days left for {name}")
    if(time_left<=30):
        print("Its time study hard!!!")
    elif(time_left>=60 and time_left<=90):
        print("you still have some time! keep going, you got it!")
    else:
        print("you have plenty time. just be consistent!")
                
        

