import sqlite3

# conn = sqlite3.connect('admins.db')
# c = conn.cursor()

# c.execute("""  CREATE TABLE problems (
#     status VARCHAR(20) NULL,
#     title VARCHAR(120),
#     description VARCHAR,
#     solution VARCHAR,
#     difficulty VARCHAR,
#     userid VARCHAR NOT NULL,
#     FOREIGN KEY(userid) REFERENCES adminsdata(rowid)
# )  """)

# c.execute("""  UPDATE  """)
# c.execute("""CREATE TABLE adminsdata 
#                 (username VARCHAR(20) NOT NULL UNIQUE,
#                 password VARCHAR(20) NOT NULL,
#                 fullname VARCHAR(20), 
#                 mobile INTEGER, 
#                 email VARCHAR(50))
#             """)



def uservalid(user):
    conn = sqlite3.connect('admins.db')
    c = conn.cursor() 
    c.execute(f" SELECT rowid,username,password,fullname,email,mobile from adminsdata WHERE username LIKE '{user}' ")
    validuser = c.fetchone()
    conn.commit()
    conn.close()
    print(">>>>>>>",validuser)
    if validuser:
        return {'id':validuser[0],'username':validuser[1],'password':validuser[2],'fullname':validuser[3],'email':validuser[4],'mobile':validuser[5]}

def addAdmin(data):
        
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute(f" INSERT INTO adminsdata VALUES {data} ")
    c.execute(f" SELECT * FROM adminsdata WHERE username LIKE '{data[0]}'")
    new = c.fetchone()
    conn.commit()
    conn.close()
    return new

def updateadmin(data, id):
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute(f" UPDATE adminsdata SET fullname = '{data['fullname']}', mobile = '{data['mobile']}', email = '{data['email']}' WHERE rowid LIKE {id} ")
    c.execute(f" SELECT rowid,username,password,fullname,email,mobile from adminsdata WHERE rowid LIKE '{id}' ")
    update = c.fetchone()
    conn.commit()
    conn.close()
    print(">>>>>>>>",update)
    if update:
        return {'id':update[0],'username':update[1],'password':update[2],'fullname':update[3],'email':update[4],'mobile':update[5]}


def addproblem(problemdata):
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute(f" INSERT INTO problems VALUES {problemdata} ")
    conn.commit()
    conn.close()

def dropproblem(id):
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute(f" DELETE FROM problems WHERE rowid LIKE {id} ")
    conn.commit()
    conn.close()
def getoneproblem(id):
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute(f"""  SELECT rowid,* FROM problems WHERE rowid LIKE {id}  """)
    singleproblem = c.fetchone()
    conn.commit()
    conn.close()
    return singleproblem

def getproblems():
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute("""  SELECT rowid,* FROM problems  """)
    allproblems = c.fetchall()
    conn.commit()
    conn.close()
    return allproblems

def getpersonal(adminid):
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute(f"""  SELECT rowid,* FROM problems WHERE userid LIKE {adminid}  """)
    allproblems = c.fetchall()
    conn.commit()
    conn.close()
    return allproblems


def search(data):
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute(f"""  SELECT rowid,* FROM problems Where title LIKE "%{data}%"  """)
    allproblems = c.fetchall()
    conn.commit()
    conn.close()
    return allproblems

def getAll():
    conn = sqlite3.connect('admins.db')
    c = conn.cursor()
    c.execute("SELECT * FROM adminsdata")
    all = c.fetchall()
    conn.commit()
    conn.close()
    return all