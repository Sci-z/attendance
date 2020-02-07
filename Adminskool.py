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



def reset():
    lcd.clear()
def checkname():
    code,text = reader.read()
    code = str(code)
    mycursor.execute('select * from student where id = "'+ code + '" ;')
    myresult = mycursor.fetchall()
    for row in myresult:
        fna = row[3]
        
    if len(myresult)>0:
        reset()
        wait = input(fna + ' already registered in school, chose an option[update info(u),remove students(r), quit(q)]')
        if wait == 'u':
            reset()
            lcd.cursor_pos = (0,0)
            lcd.write_string('change firstname[f]')
            lcd.cursor_pos = (1,0)
            lcd.write_string('change lastname[l]')
            lcd.cursor_pos = (2,0)
            lcd.write_string('change nickname[n]')
            wait = input()
            if wait == 'f':
                reset()
                lcd.write_string('Enter firstname:')
                fn = input('Firstname: ')
                mycursor.execute('update student set firstname = "' +fn+ '" where id = "'+code +'";')
                mydb.commit()
            elif wait == 'l':
                reset()
                lcd.write_string('Enter lastname:')
                ln = input('Lastname: ')
                mycursor.execute('update student set lastname = "' +ln+ '" where id = "'+code +'";')
                mydb.commit()
            elif wait == 'n':
                reset()
                lcd.write_string('Enter nickname:')
                nn = input('Nickname: ')
                mycursor.execute('update student set nickname = "' +nn+ '" where id = "'+code +'";')
                mydb.commit()
            else:
                reset()
                lcd.cursor_pos = (1,3)
                lcd.write_string('Program close.')
                print('')
                print('Program close.')   
        elif wait == 'r':
            wait = input('Do you wish to remove '+fna+' ?[y/n]')
            if wait == 'y':
                mycursor.execute('delete from student where id = '+code+';')
                mydb.commit()
            else:
                print('?')
        else:
            reset()
            lcd.cursor_pos = (1,3)
            lcd.write_string('Program close.')
            print('')
            print('Program close.')
    else:
        why = input('No student found, Registered?[y/n]')
        reset()
        lcd.write_string('No student found, \r\nRegister new?[y/n]')
        if why == 'y':
            reset()
            lcd.write_string('Enter firstname:')
            fn = input('Firstname: ')
            lcd.cursor_pos = (0,0)
            lcd.write_string('Enter lastname:')
            ln = input('Lastname: ')
            reset()
            lcd.write_string('Enter nickname:')
            nn = input('Nickname: ')
            sql = ("insert into student (id,firstname,lastname,nickname) value (%s,%s,%s,%s)")
            val = (code,fn,ln,nn)
            mycursor.execute(sql,val)
            mydb.commit()
            reset()
            lcd.write_string(nn + ' is now registered')
        else:
            reset()
            lcd.cursor_pos = (1,3)
            lcd.write_string('Program close.')
            print('')
            print('Program close.')

def checkclass():
    mycursor.execute('select count(*) from class;')
    myresult = mycursor.fetchall()
    for roww in myresult:
        num = roww[0]
        num = str(num)
    print('total class: ' + num)
    choice = input('select action[add(a),remove(r),update(u)]: ')
    if choice == 'a':
        cid = input('Class id: ')
        cn = input('Class name: ')
        tt = input('class teacher: ')
        sql2 = ("insert into class (id,name,teacher) value (%s,%s,%s)")
        val2 = (cid,cn,tt)
        mycursor.execute(sql2,val2)
        mydb.commit()
        print(tt+' is now assign to '+cn+' class('+cid+')')
    elif choice == 'r':
        cls = input('which class to take out(class name): ')
        mycursor.execute('delete from class where name = "' +cls+'";')
        mydb.commit()
        reset()
        lcd.cursor_pos = (0,0)
        lcd.write_string(cls+' class is now deleted')
    elif choice == 'u':
        reset()
        lcd.cursor_pos = (0,0)
        lcd.write_string('class name: ')
        clsn = input()
        reset()
        lcd.cursor_pos = (0,0)
        lcd.write_string('New teacher: ')
        nt = input('New teacher: ')
        mycursor.execute('update class set teacher ="'+nt+'" where name = "'+clsn+'";')
        mydb.commit()
        
    else:
        print('???')

def attend():
    act = input('select action[add(a),remove(r),update(u)]: ')
    if choice == 'a':
        id = input('student id: ')
        id2 = input('Class id: ')
        dt = input('date: ')
        mt = input('month: ')
        yt = input('year: ')
        tt = input('time[ex: 13:55:00]: ')
        total = (yt+'-'+mt+'-'+dt+' '+tt)
        
        
        sql2 = ("insert into Attendance (studentid,classid,datetime) value (%s,%s,%s)")
        val2 = (id,id2,total)
        mycursor.execute(sql2,val2)
        mydb.commit()
    elif choice == 'r':
       
    elif choice == 'u':
        
    else:
        print('???')










try:
    reset()
    what = input('Admin account, what to do[student(s),class(c),attendance(a)]: ')
    if what == 's':
        print("Swipe ID card")
        lcd.write_string('Swipe your ID card:')
        checkname()
    elif what == 'c':
        checkclass()
    elif what == 'a':
        print(':')#########################################
    else:
        print('???')
    
finally:
    GPIO.cleanup()