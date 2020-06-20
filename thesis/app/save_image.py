import mysql.connector
from mysql.connector import Error
import os
import time
import datetime



def insertImage():
  path = "./detected"
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="attendance"
  )


  mycursor = mydb.cursor()
                      ##### CHANGE TABLE NAME AND VALUES
  sql = "INSERT INTO app_recorded (id, time_detected, image, student_id) VALUES (%s, %s, %s, %s)"
  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')      
  

  for filename in os.listdir(path):
      if filename.endswith(".jpg") or filename.endswith(".png"):
          
          path = os.path.join(path, filename)
          name = os.path.splitext(filename)[0]
          name = name.replace("_"," ")
          name = name.split().pop(0)
          val = ("",timestamp,filename,name)
          mycursor.execute(sql, val)
          mydb.commit()
      else:
          continue