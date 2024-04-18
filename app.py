from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector as mq
from mysql.connector import Error
from markupsafe import Markup
import timetablegen
import random
import pandas as pd
import os
import mailing
from datetime import datetime
import pandas as pd
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

def dbconnection():
    con = mq.connect(host='localhost', database='timetable',user='root',password='root')
    return con



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/teacherregisterpage')
def teacherregisterpage():
    return render_template('teacherregister.html')

@app.route('/generateseatingpage')
def generateseatingpage():
    return render_template('generateseating.html')

@app.route('/studentregisterpage')
def studentregisterpage():
    return render_template('studentregister.html')
def custom_sort(day):
    # Define a custom sort order for the days of the week
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return day.apply(lambda x: order.index(x))


@app.route('/aviewtimetablepage')
def aviewtimetablepage():
   try:
        # Read the Excel file
        if os.path.exists('timetable.xlsx'):
            df = pd.read_excel('timetable.xlsx')
            # Convert 'Day' column to categorical with custom sort order
            df['Day'] = pd.Categorical(df['Day'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
            
            # Sort DataFrame by 'Day' column
            df_sorted = df.sort_values(by='Day', key=custom_sort)
            
            # Convert DataFrame to HTML table without index
            table_html = df_sorted.to_html(classes='table', index=False)
            
            return render_template('aviewtimetable.html', table=table_html)
        else:
            flash("Timetable not found.")
   except Exception as e:
       flash(f"An error occurred: {str(e)}")
       return render_template('aviewtimetable.html')
   

@app.route('/tviewtimetablepage')
def tviewtimetablepage():
   try:
        # Read the Excel file
        if os.path.exists('timetable.xlsx'):
            df = pd.read_excel('timetable.xlsx')
            # Convert 'Day' column to categorical with custom sort order
            df['Day'] = pd.Categorical(df['Day'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
            
            # Sort DataFrame by 'Day' column
            df_sorted = df.sort_values(by='Day', key=custom_sort)
            
            # Convert DataFrame to HTML table without index
            table_html = df_sorted.to_html(classes='table', index=False)
            
            return render_template('tviewtimetable.html', table=table_html)
        else:
            flash("Timetable not found.")
   except Exception as e:
       flash(f"An error occurred: {str(e)}")
       return render_template('tviewtimetable.html')
   

@app.route('/sviewtimetablepage')
def sviewtimetablepage():
   try:
        # Read the Excel file
        if os.path.exists('timetable.xlsx'):
            df = pd.read_excel('timetable.xlsx')
            # Convert 'Day' column to categorical with custom sort order
            df['Day'] = pd.Categorical(df['Day'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
            
            # Sort DataFrame by 'Day' column
            df_sorted = df.sort_values(by='Day', key=custom_sort)
            
            # Convert DataFrame to HTML table without index
            table_html = df_sorted.to_html(classes='table', index=False)
            
            return render_template('sviewtimetable.html', table=table_html)
        else:
            flash("Timetable not found.")
   except Exception as e:
       flash(f"An error occurred: {str(e)}")
       return render_template('sviewtimetable.html')

@app.route('/addsubjectpage')
def addsubjectpage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from teacher")
    res = cursor.fetchall()
    return render_template('addsubject.html',res=res)

@app.route('/viewteacherspage')
def viewteacherspage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from teacher right join subject on subject.tid=teacher.id")
    res = cursor.fetchall()
    return render_template('viewteachers.html',res=res)

@app.route('/addstpage')
def addstpage():
    return render_template('addst.html', title='add st')

@app.route('/reqsubstitutepage')
def reqsubstitutepage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from teacher right join subject on subject.tid=teacher.id where teacher.id!={}".format(int(session['tid'])))
    res = cursor.fetchall()
    return render_template('reqsubstitute.html',res=res)

@app.route('/substitutestatuspage')
def substitutestatuspage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from substitute left join teacher on substitute.stid=teacher.id where substitute.atid={} order by substitute.id desc".format(int(session['tid'])))
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>You Have Not Made Any Requests</h3>")
        flash(message)
    return render_template('substitutestatus.html',res=res)


@app.route('/sviewsubstituteclass')
def sviewsubstituteclass():
    con = dbconnection()
    cursor = con.cursor()
    current_date_time = datetime.now()
    # Format the date as a string
    current_date_string = current_date_time.strftime("%Y-%m-%d")
    cursor.execute("select * from substitute left join teacher on substitute.stid=teacher.id where substitute.sdate='{}' and status='{}'".format(current_date_string,"Accepted"))
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>No Substitute class for today</h3>")
        flash(message)
    return render_template('sviewsubstituteclass.html',res=res)


@app.route('/substituterequestpage')
def substituterequestpage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from substitute left join teacher on substitute.atid=teacher.id where substitute.stid={} order by substitute.id desc".format(int(session['tid'])))
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>No Requests Found</h3>")
        flash(message)
    return render_template('substituterequest.html',res=res)


@app.route('/gentpage')
def gentpage():
    return render_template('gentimet.html', title='Gen')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ltype = request.form['ltype']
        email = request.form['email']
        password = request.form['password']
        con = dbconnection()
        cursor = con.cursor()
        if ltype=='admin':
            cursor.execute("select * from admin where email='{}' and pass='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                return redirect(url_for('addsubjectpage'))
        elif ltype=='teacher':
            cursor.execute("select * from teacher where email='{}' and pass='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                session['tid']=res[0][0]
                return redirect(url_for('tviewtimetablepage'))
        else:
            cursor.execute("select * from student where email='{}' and pass='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                session['sid']=res[0][0]
                return redirect(url_for('sviewtimetablepage'))


@app.route('/studentregister', methods=['GET', 'POST'])
def studentregister():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']
    address = request.form['address']
    usn = request.form['usn']
    branch = request.form['branch']
    year = request.form['year']
    password = request.form['password']
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from student where email='{}' and usn='{}'".format(email,usn))
    res = cursor.fetchall()
    if res==[]:
        cursor.execute("insert into student (name,email,phone,gender,address,usn,branch,year,pass)values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            name,email,phone,gender,address,usn,branch,year,password
        ))
        con.commit()
        con.close()
        message = Markup("<h3>Success! Registration success!</h3>")
        flash(message)
        return redirect(url_for('loginpage'))
    else:
        message = Markup("<h3>Failed! USN or Email ID already Exists!</h3>")
        flash(message)
        return redirect(url_for('studentregisterpage'))
    

@app.route('/teacherregister', methods=['GET', 'POST'])
def teacherregister():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from teacher where email='{}'".format(email))
    res = cursor.fetchall()
    if res==[]:
        cursor.execute("insert into teacher (name,email,phone,pass)values('{}','{}','{}','{}')".format(
            name,email,phone,password
        ))
        con.commit()
        con.close()
        message = Markup("<h3>Registration success!</h3>")
        flash(message)
        return redirect(url_for('loginpage'))
    else:
        message = Markup("<h3>Failed! Email ID already Exists!</h3>")
        flash(message)
        return redirect(url_for('teacherregisterpage'))


@app.route('/addsubject', methods=['GET', 'POST'])
def addsubject():
    tid = request.form['tid']
    sname = request.form['sname']
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from subject where sname='{}' and tid={}".format(sname,int(tid)))
    res = cursor.fetchall()
    if res==[]:
        cursor.execute("insert into subject (sname,tid)values('{}',{})".format(sname,int(tid)))
        con.commit()
        con.close()
        message = Markup("<h3>Subject Added!</h3>")
        flash(message)
        return redirect(url_for('addsubjectpage'))
    else:
        message = Markup("<h3>Failed! Subject already Maped to teacher!</h3>")
        flash(message)
        return redirect(url_for('addsubjectpage'))

@app.route('/savesubstitute', methods=['GET', 'POST'])
def savesubstitute():
    tdetails = request.form['tdetails']
    stime = request.form['stime']
    sdate = request.form['sdate']
    split_data = tdetails.split(',')
    stid =  split_data[0]
    stemail =  split_data[1]
    ssubject =  split_data[2]
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from teacher where id={}".format(int(session['tid'])))
    res = cursor.fetchall()
    cursor.execute("insert into substitute (stid,atid,ssubject,sdate,stime,status)values({},{},'{}','{}','{}','{}')".format(int(stid),int(session['tid']),
                                                                                                                            ssubject,sdate,stime,"Pending"))
    con.commit()
    con.close()
    mailsubject = "REQUEST FOR CLASS SUBSTITUTION"
    mailbody = "Hi\n This is to nofify you that "+res[0][1]+" has requested for class substitution.\nKindly open the application and respond.\n\nThank you"
    mailing.mailsend(stemail.strip(),mailsubject,mailbody)
    message = Markup("<h3>Request Raised!</h3>")
    flash(message)
    return redirect(url_for('reqsubstitutepage'))

@app.route('/Deletesubstitue')
def Deletesubstitue():
    id = request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("delete from substitute where id={}".format(int(id)))
    con.commit()
    con.close()
    return redirect(url_for('substitutestatuspage'))   


@app.route('/acceptrejsubs')
def acceptrejsubs():
    id = request.args.get('id')
    status = request.args.get('status')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("update substitute set status='{}' where id={}".format(status,int(id)))
    con.commit()
    con.close()
    return redirect(url_for('substituterequestpage'))




@app.route('/generate', methods=['GET', 'POST'])
def generate():
    break_after_hours = 3
    break_duration = 15
    num_weeks = 1 
    subjects=[]
    teachers={}
    stime = request.form['stime']
    etime = request.form['etime']
    lch = request.form['lch']
    lst = request.form['lst']
    ld = request.form['ld']
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from teacher inner join subject on subject.tid=teacher.id ")
    res = cursor.fetchall()
    random.shuffle(res)
    for row in res:
        subjects.append(row[6])
        teachers[row[6]]=row[1]
    timetable = timetablegen.generate_timetable(subjects, teachers, stime, etime, int(lch), break_after_hours, break_duration, lst, int(ld), num_weeks)
    pivoted_timetable = timetablegen.pivot_timetable(timetable)
    timetablegen.export_to_excel(pivoted_timetable)
    message = Markup("<h3>Success! Time Table generated and exported to excelsheet</h3>")
    flash(message)
    return redirect(url_for('gentpage'))  




@app.route('/generateseating', methods=['GET', 'POST'])
def generateseating():
    if request.method == 'POST':
        year = request.form['year']
        branch1 = request.form['branch1']
        branch2 = request.form['branch2']
        num_rooms = int(request.form['num_rooms'])
        num_benches_per_room = int(request.form['num_benches_per_room'])

        # Calculate bench requirement
        total_students = get_total_students(year, branch1,branch2)
        required_benches = calculate_benches(total_students, num_rooms, num_benches_per_room)

        # Generate seating arrangement
        generate_seating(total_students, required_benches,branch1,branch2,year,num_benches_per_room,num_rooms)

        # Export to Excel
        #export_to_excel(seating_arrangement)
        message = Markup("<h3>Success! Seating generated and exported to excel sheet</h3>")
        flash(message)

    return render_template('generateseating.html')

def get_total_students(year, branch1, branch2):
    con = dbconnection()
    cursor = con.cursor()
    query = "SELECT COUNT(*) FROM student WHERE year='{year}' AND branch in('{branch1}','{branch2}')"
    cursor.execute(query)
    total_students = cursor.fetchone()[0]
    cursor.close()
    print("total_students ",total_students)
    return total_students

def calculate_benches(total_students, num_rooms, num_benches_per_room):
    required_benches = total_students // (num_rooms * num_benches_per_room * 2)
    if total_students % (num_rooms * num_benches_per_room * 2) != 0:
        required_benches += 1
    print(required_benches)
    return required_benches

def generate_seating(total_students, required_benches,branch1,branch2,year,num_benches_per_room,num_rooms):
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from student where year='{}' and branch='{}' order by usn asc".format(year,branch1))
    res1 = cursor.fetchall()
    print(res1)
    
    cursor.execute("select * from student where year='{}' and branch='{}' order by usn asc".format(year,branch2))
    res2 = cursor.fetchall()
    print(res2)
    columns = [branch1, branch2, 'RoomNo', 'BenchNo']
    df = pd.DataFrame(columns=columns)
    ognobenches =num_benches_per_room
    room = num_rooms
    i=0
    assignroomno=1
    assignbenchno=1
    print(res1[0])
    while ognobenches != 0 and room != 0:
        if i < len(res1) and i < len(res2):
            # Both res1 and res2 have data
            df = df.append({
                branch1: res1[i][6],
                branch2: res2[i][6],
                'RoomNo': assignroomno,
                'BenchNo': assignbenchno
            }, ignore_index=True)
        elif i < len(res1):
            # Only res1 has data
            df = df.append({
                branch1: res1[i][6],
                branch2: "",
                'RoomNo': assignroomno,
                'BenchNo': assignbenchno
            }, ignore_index=True)
        elif i < len(res2):
            # Only res2 has data
            df = df.append({
                branch1: "",
                branch2: res2[i][6],
                'RoomNo': assignroomno,
                'BenchNo': assignbenchno
            }, ignore_index=True)

        i += 1
        assignbenchno += 1
        ognobenches -= 1

        if ognobenches == 0:
            ognobenches = num_benches_per_room
            room -= 1
            assignbenchno = 1
            assignroomno+=1
            continue
    filename = 'seating'+year+branch1+branch2+'.xlsx'
    cursor.execute("insert into seating(filename,branch1,branch2,year) values('{}','{}','{}','{}')".format(filename,branch1,branch2,year))
    con.commit()
    con.close()

    df.to_excel(filename, index=False)
            
def search_usn_in_excel(usn,filename,branch):
    # Read Excel sheet
    df = pd.read_excel(filename)
    
    # Search for matching rows
    matched_rows = df[(df[branch] == usn) | (df[branch] == usn)]
    
    return matched_rows

@app.route('/sviewseat')
def sviewseat():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from student where id={}".format(int(session['sid'])))
    res = cursor.fetchall()
    usn = res[0][6]
    branch = res[0][7]
    year = res[0][8]
    cursor.execute("select * from seating where branch1='{}' or branch2='{}' and year='{}'".format(branch,branch,year))
    res2 = cursor.fetchall()
    filename=res2[0][1]
    # Search for matching rows
    matched_rows = search_usn_in_excel(usn,filename,branch)
    
    # Render HTML template and pass matched rows as context
    return render_template('sviewseat.html', rows=matched_rows.to_dict('records'))   
        
    

   

if __name__ == '__main__':
    app.run(debug=True)
