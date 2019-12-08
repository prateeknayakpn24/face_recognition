import os
import sqlite3
rec_names=[]
client='prateek3'
base_dir=os.getcwd()
database_dir=os.path.join(base_dir,'database')
if os.path.isdir(database_dir)==False:
    os.mkdir(database_dir)
conn_dir=os.path.join(database_dir,'test.sqlite')
conn = sqlite3.connect(conn_dir)

conn.execute("CREATE TABLE IF NOT EXISTS record(name TEXT,attendance INTEGER)")
for i,j in conn.execute("SELECT * FROM record"):
    rec_names.append(i)
if client not in rec_names:
    conn.execute("INSERT INTO record(name,attendance) VALUES('{}' ,23)".format(client))
else:
    rec_names.clear()

cur = conn.cursor()
cur.execute("UPDATE record SET attendance=attendance+10 WHERE name='{}'".format(client))
print("{} row updated".format(cur.rowcount))
cur.execute("SELECT * from record")
data = cur.fetchall()
for name,attendance in data:
    print(name,end=' ')
    print(attendance)
cur.close()
conn.commit()
conn.close()
''''cur = conn.cursor()
table='create table attendence_record(name text NOT NULL,attendance integer)'
query='insert into attendence_record(name,attendence) values(?,?)'
val=('prateek',0)
cur.execute(table)
cur.execute(query,val)
conn.commit()'''