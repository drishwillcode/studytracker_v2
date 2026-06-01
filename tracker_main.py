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
def askusername():
    un=input("enter username")
    return un
def askpwd():
    pwd=input("enter password")
    return pwd
def login():
    un=askusername
    
if var==1:
elif var==2:    
        
        

