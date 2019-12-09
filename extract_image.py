import sqlite3
import os
import cv2
ids=[]
roi_gray=[]
rec_names=[]
print('IT IS RECOMMENDED TO SHAKE YOUR HEAD VERTICALLY FOR BETTER COLLECTION OF DATA')
base_dir = os.getcwd()
if os.path.isdir('images')==False:
    os.mkdir('images')
images_dir = os.path.join(base_dir,'images')
database_dir=os.path.join(base_dir,'database')
conn_dir=os.path.join(database_dir,'attendance_database.sqlite')
if os.path.isdir(database_dir)==False:
    os.mkdir(database_dir)

#Creating a table:
conn=sqlite3.connect(conn_dir)
conn.execute("CREATE TABLE IF NOT EXISTS record(name,attendance)")
conn.commit()
conn.close()

def insert_values(name):
    conn=sqlite3.connect(conn_dir)
    for i,j in conn.execute("SELECT * FROM record"):
        rec_names.append(i)
    if name not in rec_names:
        conn.execute("INSERT INTO record VALUES('{}',0)".format(names))
        rec_names.clear()
    else:
        rec_names.clear()
    conn.commit()
    conn.close()

def display_table():
    conn=sqlite3.connect(conn_dir)
    cur=conn.cursor()
    cur.execute("SELECT * FROM record")
    data=cur.fetchall()
    print(data)


while(True):
    name = input('Enter your name')
    id=input('Enter your id')
    names=name+'_'+id
    for root,dirs,files in os.walk(images_dir):
        if not os.listdir(images_dir):
            os.mkdir(images_dir+'/'+names)
        else:
            for i in dirs:
                name_id=i.split('_')
                ids.append(name_id[1])

    if id in ids:
       print("Incorrect ID!.Please enter your correct ID number:")
       ids.clear()
    else:
       break

print(names)
insert_values(names)
display_table()
name_dir=os.path.join(images_dir, names)
if os.path.isdir(name_dir) == False:
    os.mkdir(name_dir)

c=-1
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
while(c<=60):
    if c==-1:
        print('Creating Dataset...')
        c+=1
    ret, frame = cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=1)
    for (x,y,w,h) in faces:
        roi_gray=gray[y-10:y+h+20,x-10:x+w+20]
        path = name_dir
        cv2.imwrite(os.path.join(path,"{0}_{1}.jpg".format(id,c)),roi_gray)
        cv2.rectangle(frame,(x-10,y-10),(x+w+20,y+h+10),(0,0,255),2)
        c+=1
    cv2.imshow('Creating Dataset...',frame)
    cv2.waitKey(2)

print("Dataset Created")
cap.release()
cv2.destroyAllWindows()
