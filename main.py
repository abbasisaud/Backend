from datetime import datetime
from flask import Flask,jsonify,request
from flask_restful import  Api, Resource
import pyodbc
from datetime import datetime
import functions

from flask import flash
import json
import base64
import os

app=Flask(__name__)
api=Api(app)
countdata={}
visiterlist=[]

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL SERVER};"
    "Server=DESKTOP-T5JLV55;"
    "Database=VisitorTrackingSystem;"
    "Trusted_Connection=yes;"
)

@app.route('/login/<string:uname>/<string:pasword>')
def login(uname,pasword):
    cursor = conn.cursor()
    data=cursor.execute('select * from Users')    
    res="user not found"
    for i in data:       
        if uname in i:
            if pasword in i:
                if 'guard' in i:
                    res='guard'
                elif 'admin'in i:
                    res='admin'
                elif 'person' in i:
                    res='person'
            else:
                res='password is in correct'
    return res                



@app.route('/CurrentVisiters', methods=['GET'])
def currentVisitors():
    d = []
    cur = conn.cursor()
    cur.execute("select * from Visitors")
    rows = cur.fetchall()
    for row in rows:
       l={'id':row[0],'name':row[1],'uri':row[2],'cnic':row[3],'date':row[4],'Timein':row[5],'Timeout':row[6],'Destination':row[7]}
       d.append(l)
    resp = json.dumps(d,default=str)
    # resp=json.loads(d) 
    return resp

@app.route('/insert', methods=['POST','GET'])
def insert():
    name = request.form['v_name']
    Destination = request.form['destination']
    visiterlist.append(name)
    descam=functions.DestinationCam(Destination)
    path=functions.getPath(e=descam)
    cameras=path
    names=name
    counter = {name: {camera: 0 for camera_list in cameras for 
                        camera in camera_list} for name in names}
    countdata.update(counter)
    cnic = request.form['v_cnic']    
    vdate = datetime.now().date()
    timein = datetime.now().time().strftime("%H:%M:%S")
      
    # unique directory creation
    directory = name
    # parent_dir = r"C:\Users\Saud\Desktop\FaceRecognition2\dataset"
    parent_dir = r"C:\Users\Saud\Desktop\ProjectApi\All_pics"
    path = os.path.join(parent_dir,directory)
    if not os.path.exists(path):
        os.makedirs(path)
    filename=' '
    i=1
    for field, data in request.files.items(True):      
        # print(data)       
        uniquefile = str(i).replace(".", "")
        split = str(data.filename).split(".")
        ext = split[len(split) - 1]
        filename=f"{uniquefile}.{ext}"
        finalfilepath = f"All_pics\{name}\{uniquefile}.{ext}"
        data.save(finalfilepath)
        i+=1
    image=(os.path.join(path,filename))
    cursor = conn.cursor()
    try:
        insert_user_cmd ="""INSERT INTO visitors (v_name,v_pic,v_cnic,vdate,timein,time_out,vdestination) VALUES(?,?,?,CONVERT(DATE,?,120),CONVERT(Time,?, 0),null,?)"""
        cursor.execute(insert_user_cmd, (name, image, cnic,vdate,timein,Destination))
        conn.commit()
        response = jsonify(message='User added successfully .')
        response.status_code = 200
        return response
    except ValueError:
        response = jsonify(message='Invalid Input')
        return response



@app.route('/saveAlerts/<string:name>/<int:status>/<string:cam>', methods=['POST'])
def Alertdata(name,status,cam):
    cursor = conn.cursor()
    timein = datetime.now().time().strftime("%H:%M:%S")
    # insert_user_cmd = """insert into Alerts values(%s,%s)"""
    cursor.execute("insert into alerts (name,status,DetectCam,detectTime) values ('"+(name)+"' ,'"+str(status)+"','"+(cam)+"',CONVERT(Time,'"+timein+"', 0))")
    cursor.commit()
    response = ('data added successfully.')
    # response.data = cursor.lastrowid
    return response

@app.route('/getNames', methods=['GET'])
def getAlertData():
    d = []
    cur = conn.cursor()
    cur.execute("select * from alerts")
    rows = cur.fetchall()
    i=1
    for row in rows:
        l = {'id':i,'name':row[1].strip()}
        d.append(l)
        i+=1
    # resp = json.dumps(d,default=str)
    # resp=json.loads(resp)
    return jsonify(d)

@app.route('/getAlertVisitor/<string:name>', methods=['GET'])
def getAlertVisitor(name):
    d = []
    cur = conn.cursor()
    cur.execute("select * from Visitors where v_name='"+(name)+"'")
    rows = cur.fetchall()
    for row in rows:
       l={'id':row[0],'name':row[1],'uri':row[2],'cnic':row[3],'date':row[4],'Timein':row[5],'Timeout':row[6],'Destination':row[7]}
       d.append(l)
    resp = json.dumps(d,default=str)
    # resp=json.loads(d) 
    return resp 

    
@app.route('/getDestination', methods=['GET'])
def getDestination():
    d = []
    cur = conn.cursor()
    cur.execute("select * from Destination")
    rows = cur.fetchall()
    i=1
    for row in rows:
        l = {'id':i,'Destination':row[1],'Total Visitors':row[2]}
        d.append(l)
        i+=1
    # resp = json.dumps(d,default=str)
    # resp=json.loads(resp) 
    return jsonify(d)
    
@app.route('/getDestinationVisiterMonth/<string:Destination>/<int:month>', methods=['GET'])
def getDestinationVisitorByMonth(Destination,month):
    d = []
    cur = conn.cursor()
    cur.execute("select * from Visitors where vdestination='"+(Destination)+"'and MONTH(vdate)='"+str(month)+"'")
    rows = cur.fetchall()
    for row in rows:
       l={'id':row[0],'name':row[1],'uri':row[2],'cnic':row[3],'date':row[4],'Timein':row[5],'Timeout':row[6],'Destination':row[7]}
       d.append(l)
    resp = json.dumps(d,default=str)
    # resp=json.loads(d) 
    return resp

@app.route('/getDestinationByMonth/<string:month>', methods=['GET'])
def getDestinationByMonth(month):
    d = []
    cur = conn.cursor()
    # cur.execute("select * from Visitor where VDestination='"+(Destination)+"'")
    cur.execute("SELECT vdestination, COUNT(vdestination) as c FROM Visitors where MONTH(vdate)='"+(month)+"' GROUP BY vdestination order by(c) desc")

    rows = cur.fetchall()
    i=1
    for row in rows:
       l={'id':i,'Destination':row[0],'Count':row[1]}
       d.append(l)
       i+=1
    # resp = json.dumps(d,default=str)
    # resp=json.loads(d) 
    return jsonify(d)

@app.route('/addCamera/<string:name>/<string:url>/<string:details>', methods=['POST'])
def AddCamera(name,url,details):
    cursor = conn.cursor()
    cursor.execute("insert into Camera (name,url,details) values('"+(name)+"','"+(url)+"','"+(details)+"')")
    cursor.commit()
    response = ('Camera added successfully.')
    # response.data = cursor.lastrowid
    return response

@app.route('/addDestination/<string:name>/<string:camera>', methods=['POST'])
def AddDes(name,camera):
    cursor = conn.cursor()
    cursor.execute("insert into Destination (dname,ConnectedCam) values('"+(name)+"','"+(camera)+"')")
    cursor.commit()
    response = ('destination added successfully.')
    # response.data = cursor.lastrowid
    return response

@app.route('/getAllCameras', methods=['GET'])
def getAllCameraa():
    d = []
    cur = conn.cursor()
    cur.execute("select name from Camera")
    rows = cur.fetchall()
    for row in rows:
        l = {row[0]}
        d.append(l)
    resp = json.dumps(d,default=str)
    # =json.loads(resp) 
    return (resp)

@app.route('/camtocamtime', methods=['GET'])
def gettime():
    d = []
    cur = conn.cursor()
    cur.execute("select camfrom,camto,time from CamToCamTime")
    rows = cur.fetchall()
    for row in rows:
        l = {row[0],row[1],str(row[2])}
        d.append(l)
    resp = json.dumps(rows,default=str)
    # =json.loads(resp) 
    return (resp)
@app.route('/getDescam/<string:destination>', methods=['GET'])
def getDescam(destination):
    d = []
    cur = conn.cursor()
    cur.execute("select connectedcam from destination where dname='"+(destination)+"'")
    rows = cur.fetchall()
    for row in rows:
        l = {row[0].strip()}
        d.append(l)      
    resp = json.dumps(d,default=str)
    # resp=json.loads(resp)
    return resp

@app.route('/getDesbyname/<string:name>', methods=['GET'])
def getDesByname(name):
    d = []
    cur = conn.cursor()
    cur.execute("select vdestination from visitors where v_name='"+(name)+"'")
    rows = cur.fetchall()
    for row in rows:
        l = {row[0].strip()}
        d.append(l)      
    resp = json.dumps(d,default=str)
    # resp=json.loads(resp)
    return resp

@app.route('/updatetimeout/<string:name>', methods=['POST'])
def settimeout(name):
    timeout = datetime.now().time().strftime("%H:%M:%S") 
    cur = conn.cursor()
    try:
        cur.execute("update visitors set time_out='"+(timeout)+"' where v_name='"+(name)+"'")
        cur.commit()
        response =jsonify('time updated')
        response.status_code = 200
    except ValueError:
        response='name not found' 
    return response
if __name__ == "__main__":
    app.run(debug=True)
    
   
    
