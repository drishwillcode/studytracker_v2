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
    if u_id==None:
        pass
    else:
        cur.execute("insert into ch_progress(user_id, ch_id) select {}, ch_id from chapters".format(u_id))

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
    if(time_left<=30 and time_left>0):
        print("Its time study hard!!!")
    elif(time_left>=60 and time_left<=90):
        print("you still have some time! keep going, you got it!")
    elif(time_left<=0):
        print("exam ended", (-1)*time_left, "days ago!!!")
    else:
        print("you have plenty time. just be consistent!")
                
 #---FUNCTION TO DISPLAY LIST OF CHAPTERS---
def chap_list():
            ch_options={1:'all chapters',
                        2:'completed chapters',
                        3:'pending chapters',
                        4:'mathematics chapters',
                        5:'physics chapters',
                        6:'chemistry chapters'}
            for i in ch_options:
                print(i,"  :      ",ch_options[i])
            pref1=int(input("please enter your preference:"))
            if(pref1==1):
                cur.execute('select * from chapters ;')
                for i in cur.fetchall():
                    print(i)
            elif(pref1==2):
                query=('''select chapters.ch_name
    from chapters
    join ch_progress
    on ch_progress.ch_id=chapters.ch_id
    where ch_progress.status="finished"
    and ch_progress.user_id={}
    ;
    '''.format(u_id))
                for i in cur.fetchall():
                    print(i)
            elif(pref1==3):
                cur.execute('''select chapters.ch_name
    from chapters
    join ch_progress
    on ch_progress.ch_id=chapters.ch_id
    where ch_progress.status="pending"
    and ch_progress.user_id={}
    ;
    '''.format(u_id))
                for i in cur.fetchall():
                    print(i)
            elif(pref1==4):
                cur.execute('''select chapters.ch_name
    from chapters
    join ch_progress
    on ch_progress.ch_id=chapters.ch_id
    where chapters.sub="mathematics"
    and ch_progress.user_id={}
    ;
    '''.format(u_id))
                for i in cur.fetchall():
                    print(i)
            elif(pref1==5):
                cur.execute('''select chapters.ch_name
    from chapters
    join ch_progress
    on ch_progress.ch_id=chapters.ch_id
    where chapters.sub="physics"
    and ch_progress.user_id={}
    ;
    '''.format(u_id))
                for i in cur.fetchall():
                    print(i)
            elif(pref1==6):
                cur.execute('''select chapters.ch_name
    from chapters
    join ch_progress
    on ch_progress.ch_id=chapters.ch_id
    where chapters.sub="chemistry"
    and ch_progress.user_id={}
    ;
    '''.format(u_id))
                for i in cur.fetchall():
                    print(i)


#---FUNCTION TO INPUT TEST SCORES---
def insert_score():
            name=input("what was the name of the test?")
            date=input("test date? dd-mm-yyy")
            mark=int(input("what were the maximum marks?"))
            ttl=int(input("total marks obtained by you?"))
            phy=int(input("marks obtained in physics?"))
            pmax=int(input("enter max marks for physics?"))
            math=int(input("marks obtained in mathematics?"))
            mmax=int(input("enter max marks for mathematics?"))
            chem=int(input("marks obtained in chemistry?"))
            cmax=int(input("enter max marks for chemistry?"))
            typ=input("test type? (mock, subject, etc)")
            cur.execute('''insert into tests(user_id,name,date,type)
    values(%s,'%s','%s','%s')''',(u_id,name,date,typ))
            con.commit()
            testid=cur.lastrowid()
            cur.execute('''insert into test_result(test_id, subject, marks, maxmarks)''')

#---SHOW AVAILABLE FUNCTIONS---
while True:        
    print("what would you like to do today?")
    #available tasks
    func={1:"edit exam list",
          2:"show exam list",
          3:"time remaining till exam" ,
          4:"show list of chapters",
          5:"update syllabus completion",
          6:"insert test scores",
          7:"show test analysis",
          8:"show syllabus progress",
          9:"exit"}
    for i in func:
        print(i,"   :        ",func[i])
    task=int(input("enter the number:\n"))
    if (task==1):
        edit_exam()
        
    elif(task==2):
        exam_list()
        
    elif(task==3):
        day_till_ex()
        
    elif(task==4):
        chap_list()
        
    elif(task==9):
        print("study well!\n----------\n")
        break
    else:
        print("invalid input")
    print("\n----------\n\n")    
    time.sleep(2)       
con.close()

