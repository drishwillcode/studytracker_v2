import pymysql
import time
import datetime
import matplotlib.pyplot as plt


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
           pass
def signup():
    username=input("select a username")
    pwd=input("select a password")
    query=('''insert into user_info (username,password)
           values('{}','{}') '''.format(username,pwd))
    cur.execute(query)
    con.commit()
    print("new account successful!")
    print("continue loging in")
    return login()
    
if var==1:
    u_id=login()
    while u_id==None:
        print("incorrect username or password, try again")
        u_id=login()
        if u_id!=None:
            break
        
    print(u_id)
elif var==2:
    u_id=signup()
    while u_id==None:
        print("incorrect username or password, try again")
        u_id=login()
        if u_id!=None:
            break
    print(u_id)
    cur.execute("insert into ch_progress(user_id, ch_id) select {}, ch_id from chapters".format(u_id))
    con.commit()
    print("executed")
    
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
    name=input('enter name of your test/exam:')
    typ=input("enter test type (full OR subject)")
    date=input("enter date of test(yyyy-mm-dd)")
    cur.execute("insert into tests(user_id,name,date,type) values(%s,%s,%s,%s)",(u_id,name,date,typ))
    con.commit()
    print("saved in test")
    testid=cur.lastrowid
    while True:
        print("~enter details of the subjects")
        sub=input("enter subject name (press enter to end):")
        if (sub==""):
            break
        else:
            maxx=int(input("enter maximum marks:"))
            ob=int(input("enter marks obtained by you:"))
            cur.execute('''insert into test_result(test_id, subject, marks, maxmarks)
            values(%s,%s,%s,%s)''',(testid,sub,ob,maxx))
            con.commit()
            print("saved in test result wala")


#---FUNCTION TO UPDATE SYLLABUS---
def update_syll():
        def finished():
            ch=input("enter chapter ids you have finished. eg. 2,3,41")
            lst=ch.split(",")
            ch_lst=[]
            for i in lst:
                ch_lst.append(int(i)) 
            for j in ch_lst:     
                cur.execute("update ch_progress set status='FINISHED' where ch_id in (%s) and user_id=(%s) ;",(j,u_id)) 
                con.commit()
        def in_progress():
            ch=input("enter chapter numbers og the chapters in progress. eg. 2,3,41")
            lst=ch.split(",")
            ch_lst=[]
            for i in lst:
                ch_lst.append(int(i)) 
            for j in ch_lst:     
                cur.execute("update ch_progress set status='IN PROGRESS' where ch_id in (%s) and user_id=(%s) ;",(j,u_id))
                con.commit()
        def pending():
            ch=input("enter chapter numbers of pending chapters. eg. 2,3,41")
            lst=ch.split(",")
            ch_lst=[]
            for i in lst:
                ch_lst.append(int(i)) 
            for j in ch_lst:     
                cur.execute("update ch_progress set status='PENDING' where ch_id in (%s) and user_id=(%s) ;",(j,u_id)) 
                con.commit()
        updt_options={1:"update completed chapters ",
                   2:"update chapters in progress",
                   3:"update pending chapters ",
                       4:"finish updating syllabus progress"}
        for i in updt_options:
             print(i,"  :      ",updt_options[i])
        while True:    
             updt_pref=int(input("enter your preference:"))
             if updt_pref==1:
                 finished()
             elif updt_pref==2:
                 in_progress()
             elif updt_pref==3:
                 pending()
             elif updt_pref==4:
                 break
             else:
                 print("invalid input ")
        print("updated succesfully!")

#---FUNCTION TO SHOW TEST ANALYSIS---
def test_analysis():
    #ask which graph/analysis user wants to see
    ana_options={1:"overall percentage",
                 2:"physics scores",
                 3:"chemistry scores",
                 4:"mathematics score",
                 5:"all of the above",}
    for i in ana_options:
        print(i,"   :      ",ana_options[i])
    ana_pref=int(input("enter your preference:"))
    print('----------\n')

     
    def ana_chem():
            query1=(f'''select t.name
        from tests t
        join test_result tr
        on t.test_id=tr.test_id
        where t.user_id={u_id}
        and t.type='subject'
        and tr.subject="chemistry";
        ''')
            cur.execute(query1)
            namedata=cur.fetchall()
            name=[i[0] for i in namedata]

            query2=(f'''select tr.marks,tr.maxmarks
        from test_result tr
        join tests t
        on t.test_id=tr.test_id
        where tr.subject='chemistry'
        and t.type='subject'
        and t.user_id={u_id}
        ;
        ''')
            cur.execute(query2)
            percdata=cur.fetchall()
            perc=[i[0]/i[1]*100 for i in percdata]

            plt.title("CHEMISTRY SCORES")
            plt.xlabel("test name")
            plt.ylabel("physics percentage")
            plt.plot(name,perc,marker="o")
            plt.show()

    def ana_phy():
          query1=(f'''select t.name
        from tests t
        join test_result tr
        on t.test_id=tr.test_id
        where t.user_id={u_id}
        and t.type='subject'
        and tr.subject="physics";
        ''')
          cur.execute(query1)
          namedata=cur.fetchall()
          name=[i[0] for i in namedata]
            
          query2=(f'''select tr.marks,tr.maxmarks
        from test_result tr
        join tests t
        on t.test_id=tr.test_id
        where tr.subject='physics'
        and t.type='subject'
        and t.user_id={u_id}
        ;
        ''')
          cur.execute(query2)
          percdata=cur.fetchall()
          perc=[i[0]/i[1]*100 for i in percdata]

          plt.title("PHYSICS SCORES")
          plt.xlabel("test name")
          plt.ylabel("physics percentage")
          plt.plot(name,perc,marker="o")
          plt.show()  
    def ana_math():
          query1=(f'''select t.name
        from tests t
        join test_result tr
        on t.test_id=tr.test_id
        where t.user_id={u_id}
        and t.type='subject'
        and tr.subject="mathematics";
        ''')
          cur.execute(query1)
          namedata=cur.fetchall()
          name=[i[0] for i in namedata]

          query2=(f'''select tr.marks,tr.maxmarks
        from test_result tr
        join tests t
        on t.test_id=tr.test_id
        where tr.subject='mathematics'
        and t.type='subject'
        and t.user_id={u_id}
        ;
        ''')
          cur.execute(query2)
          percdata=cur.fetchall()
          perc=[i[0]/i[1]*100 for i in percdata]

          plt.title("MATHEMATICS SCORES")
          plt.xlabel("test name")
          plt.ylabel("physics percentage")
          plt.plot(name,perc,marker="o")
          plt.show()
    def ana_overall():
          query=(f'''select t.name,sum(tr.marks),sum(tr.maxmarks)
        from tests t
        join test_result tr
        on t.test_id=tr.test_id
        where t.user_id={u_id}
        and t.type="full"
        group by t.test_id;
        ''')
          cur.execute(query)
          data=cur.fetchall()
          name=[i[0] for i in data]
          perc=[i[1]/i[2]*100 for i in data]
          plt.title("OVERALL SCORES")
          plt.xlabel("test name")
          plt.ylabel("percentage")
          plt.plot(name,perc,marker="o")
          plt.show()
          
    if (ana_pref==1):
        ana_overall()
    elif(ana_pref==2):
        ana_phy()
    elif(ana_pref==3):
        ana_chem()
    elif(ana_pref==4):
         ana_math()
    elif(ana_pref==5):
         ana_overall()
         ana_phy()
         ana_chem()
         ana_math()
    else:
        print("wrong input!")

        
#function to show syllabus progress:
def syll_progress():
        cur.execute(f"select count(*) from ch_progress where status='pending' and user_id={u_id};")
        a=cur.fetchone()[0]
        cur.execute(f"select count(*) from ch_progress where status='finished' and user_id={u_id}; " )
        b=cur.fetchone()[0]
        cur.execute(f"select count(*) from ch_progress where status='in progress' and user_id={u_id};")
        c=cur.fetchone()[0]
        y=[a,b,c]
        lab=["pending",'finished','in progress']
        plt.pie(y,labels=lab)
        plt.show()

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
        
    elif(task==5):
        update_syll()
        
    elif(task==6):
        insert_score()

    elif(task==7):
        test_analysis()

    elif(task==8):
        syll_progress()  
        
    elif(task==9):
        print("study well!\n----------\n")
        
        break
    else:
        print("invalid input")
    print("\n----------\n\n")    
    time.sleep(2)
    
con.close()

