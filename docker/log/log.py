import sys
sys.path.append("/opt/homebrew/lib/python3.9/site-packages")
import paho.mqtt.client as mqtt
import json
import pymysql
from datetime import datetime, timedelta

db = pymysql.connect(
    host="host.docker.internal",
    port=3333,
    user="abcd",
    passwd="1234",
    db="plc",
    charset="utf8",
)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


trackflag = True
twoflag = False

def on_message(client, userdata, msg):
    today = datetime.today().strftime("%Y-%m-%d")
    global trackflag
    global twoflag
    data = msg.payload.decode("utf-8")
    data_dict = json.loads(msg.payload)
    cursor = db.cursor()
    sql = """INSERT INTO malfunction (date,normal,defect)
        SELECT current_date(),0,0
        from dual
        WHERE NOT EXISTS ( SELECT * FROM malfunction WHERE date = (%s))"""
    cursor.execute(sql,today)
    sql = """INSERT INTO operation (date,first,second,third)
                SELECT current_date(),0,0,0
                from dual
                WHERE NOT EXISTS ( SELECT * FROM operation WHERE date = (%s))"""
    cursor.execute(sql, today)
    sql = """INSERT INTO hastrack (date,normal,defect)
    SELECT current_date(),0,0
    from dual
    WHERE NOT EXISTS ( SELECT * FROM hastrack WHERE date = (%s))"""
    cursor.execute(sql, today)
    TrackId = None
    if data_dict["Wrapper"][2]["value"] and trackflag:
        print("ok")
        trackflag = False
        dataTime = datetime.strptime(
            data_dict["Wrapper"][40]["value"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        start_time = dataTime
        end_time = start_time + timedelta(seconds=31)
        cursor = db.cursor()
        sql = "INSERT INTO track (start, end) VALUES (%s, %s)"
        cursor.execute(sql, (start_time, end_time))
        print(1)
        sql = """UPDATE operation SET first = first + 1 WHERE date = (%s)"""
        cursor.execute(sql,today)
        db.commit()
    elif data_dict["Wrapper"][2]["value"] == False:
        trackflag = True
    Datetime = datetime.strptime(
        data_dict["Wrapper"][40]["value"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    sql = "SELECT * FROM track order by id desc limit 1";
    cursor.execute(sql)
    r = cursor.fetchone()
    Start = data_dict["Wrapper"][0]["value"]
    No1Action = data_dict["Wrapper"][2]["value"]
    No2InPoint = data_dict["Wrapper"][18]["value"]
    No3Motor1 = int(data_dict["Wrapper"][34]["value"])
    No3Motor2 = int(data_dict["Wrapper"][35]["value"])
    Dicevalue = int(data_dict["Wrapper"][38]["value"])
    sql = """SELECT * FROM malfunction where date = (%s)"""
    cursor.execute(sql, today)
    row = cursor.fetchone()
    print(data_dict["Wrapper"][3]["name"])
    if not twoflag and data_dict["Wrapper"][3]["value"]:
        twoflag = True
    if twoflag and not data_dict["Wrapper"][3]["value"]:
        print(2)
        sql = """UPDATE operation SET second = second + 1 WHERE date = (%s)"""
        cursor.execute(sql, today)
        twoflag = False
    if int(No3Motor2) > 0 and int(No3Motor2) <= 18000000 and int(No3Motor1) > 0 and int(No3Motor1) <= 1150000:
        sql = """UPDATE malfunction set normal = (%s) where date = (%s)"""
        cursor.execute(sql, (int(row[1]) + 1, row[0]))
    elif int(No3Motor2) < 0 or int(No3Motor2) > 18000000 or int(No3Motor1) < 0 or int(No3Motor1) > 1150000:
        sql = """UPDATE malfunction set detect = (%s) where date = (%s)"""
        cursor.execute(sql,(int(row[2]) + 1, row[0]))
    if Datetime >= r[1] and Datetime <= r[2]:
        TrackId = r[0]
    sql = """SELECT * FROM hastrack where date = (%s)"""
    cursor.execute(sql,today)
    row = cursor.fetchone()
    print(row)
    if not TrackId:
        sql = """UPDATE hastrack set defect = (%s) where date = (%s)"""
        cursor.execute(sql,(int(row[2]) + 1 , row[0]))
    else:
        sql = """UPDATE hastrack set normal = (%s) where date = (%s)"""
        cursor.execute(sql,(int(row[1]) + 1, row[0]))
    print(Datetime, Start, No1Action, No2InPoint, No3Motor1, No3Motor2, Dicevalue,TrackId)
    sql = """INSERT INTO record (Datetime,Start,No1Action,No2InPoint,No3Motor1,No3Motor2,Dicevalue,TrackId) values (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(
        sql, (Datetime, Start, No1Action, No2InPoint, No3Motor1, No3Motor2, Dicevalue,TrackId))
    db.commit()



# 새로운 클라이언트 생성
client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_message(발행된 메세지가 들어왔을 때)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# address : localhost, port: 1883 에 연결
client.connect("192.168.0.128", 1883)
client.subscribe("edukit/robotarm", 1)

client.loop_forever()