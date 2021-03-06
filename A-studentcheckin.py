import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="atten"
)

from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
print(mydb)

mycursor = mydb.cursor()

from flask import Flask

app = Flask(__name__)

def reset():
    lcd.clear()
    
    
    
    
@app.route("/")
def home():
    myhtml = '''
<html>
<body bgcolor ="fadegray">
<table>
<thead bgcolor ="red"><tr><th>studentid</th><th>classid</th><th>datetime</th></tr></thead>
<tbody>
'''.format()
    while round > 0:
        
        #do it
        myhtml += '<tr bgcolor ="lightblue"><td>{x}</td><td>{y}</td><td>{z}</td></tr>'
        round = round - 1
    return myhtml



try:
    reset()
    lcd.write_string('Swipe your ID card:')
    code,text = reader.read()
    code = str(code)
    mycursor.execute('select * from student where id = "'+ code + '" ;')
    myresult = mycursor.fetchall()
    for row in myresult:
        nna = row[3]
        lna = row[2]
        fna = row[1]
    print('Students: '+fna+' '+lna+' '+'('+nna+')')
    reset()
    lcd.write_string(fna+' '+lna+'('+nna+')\n\r\ninsert class code:')
    
    mycursor.execute('select * from class;')
    myresult2 = mycursor.fetchall()
    mycursor.execute('select count(*) from class;')
    myresult22 = mycursor.fetchall()
    myresult22 = str(myresult22)
    for roww in myresult2:
        classcode = roww[0]
    print('total class: '+myresult22)
    print(myresult2)
    
    sel = input('insert your class code: ')
    mycursor.execute('select * from class;')
    myresultt = mycursor.fetchall()
    for rowww in myresultt:
        classname = roww[1]
    
    
    
    reset()
    hey =('insert into Attendance(studentid,classid,datetime) value(%s,%s,Now());')
    you =(code,sel)
    mycursor.execute(hey,you)
    mydb.commit()
    print(nna+' is now in class:'+classname)
    reset()
    lcd.write_string(fna+' '+lna+'('+nna+')\n\rcheckin to '+classname)
    mycursor.execute('select * from Attendance where datetime = Now();')
    myresultt = mycursor.fetchall()
    my = str(myresultt)
    x = my[3:15]
    y = my[19:22]
    z = my[26:45]
    if __name__ == "__main__":
        app.run()
finally:
    GPIO.cleanup()