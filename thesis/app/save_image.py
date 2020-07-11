import mysql.connector
from mysql.connector import Error
import os
import time
import datetime
from thesis.settings import BASE_DIR
import re

def insertImage():
  path = BASE_DIR + "/app/detected"
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="attendance"
  )


  mycursor = mydb.cursor()
                      ##### CHANGE TABLE NAME AND VALUES
  sql = "INSERT INTO app_recorded (id, student_name,time_detected, image) VALUES (%s, %s, %s,%s)"
  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')      
  

  for filename in os.listdir(path):
      if filename.endswith(".jpg") or filename.endswith(".png"):
          
          path = os.path.join(path, filename)
          name = os.path.splitext(filename)[0]
          name = name.replace("_"," ")
          name = re.sub(r"\d", " ", name)
          name = re.sub("-", "", name)
          val = ("",name,timestamp,filename)
          mycursor.execute(sql, val)
          mydb.commit()
      else:
          continue