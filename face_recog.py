import cv2
import pickle
import sqlite3
import os
k=False
with open('names.pickle','rb') as f:
    dict_names=pickle.load(f)
    #names={v:k for k,v in og_names.items()}

print(dict_names)
face_cascade=cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cap=cv2.VideoCapture(0)
ret,frame=cap.read()

dir=os.path.join(os.getcwd(),"database")
conn_dir=os.path.join(dir,'attendance_database.sqlite')
conn=sqlite3.connect(conn_dir)
cur=conn.cursor()

while (ret==True):
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)

    for (x,y,w,h) in faces:
        #print(x,y,w,h)
        roi_gray=gray[y:y+h,x:x+w]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        id_,conf=recognizer.predict(roi_gray)
        if conf<=100:
            name=dict_names[str(id_)]
            query_name=name+'_'+str(id_)
            print("Face detected:{}   Accuracy:{}".format(name,conf))
            cv2.putText(frame,name,(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
            cur.execute("UPDATE record SET attendance=attendance+1 WHERE name='{}'".format(query_name))
            print("{} row updated".format(cur.rowcount))
            cur.execute("SELECT * FROM record")
            data=cur.fetchall()
            print(data)
            conn.commit()
            conn.close()
            k=True
        else:
            print("Your prediction exceeded 100.   Accuracy:{}".format(conf))

    cv2.imshow('frame',frame)
    if k == True:
        break
    if cv2.waitKey(2)&0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
