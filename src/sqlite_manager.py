'''
Created on Jul 7, 2021

@author: adrian
'''
import sqlite3
import datetime
import json

def energy_load(loras):
    conn = sqlite3.connect('meter_db.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS meter_table ')
    #cur.execute("CREATE TABLE meter_table (meter_id STRING, energy INTEGER, date STRING, state BOOLEAN)")  #Original
    cur.execute("CREATE TABLE meter_table (meter_id STRING, energy INTEGER, state BOOLEAN)")              #Para el test
    conn.commit()
    for i in range(len(loras)):
        nuevo = 1
        #print(loras[i]['loraid'])
        #print(loras[i]['slaves'])
        if(loras[i]['loraid']<16):
            msb_4 = '0'+str(hex(loras[i]['loraid']).split('x')[-1])
        else:
            msb_4 = str(hex(loras[i]['loraid']).split('x')[-1])

        for s in range(len(loras[i]['slaves'])):
            lsb_2 = str(0)+str(hex(loras[i]['slaves'][s]).split('x')[-1])
            meter_id = str('00'+msb_4+lsb_2)
            date = datetime.datetime.now()
            cur.execute('SELECT meter_id FROM meter_table')
            for row in cur:
                nuevo = 1
                if(row[0] == meter_id): 
                    nuevo = 0
                    break               
            if(nuevo==1):
                #print("NUEVO MEDIDOR")
                #cur.execute("INSERT INTO meter_table(meter_id,energy,date,state) VALUES(?,?,?,?)",(meter_id,0,date,False))   #Original
                cur.execute("INSERT INTO meter_table(meter_id,energy,state) VALUES(?,?,?)",(meter_id,0,1))              #Modificado para el test
                conn.commit() 
            nuevo = 1
    cur.close()


def load_json(id, write_api_key):
    conn = sqlite3.connect('meter_db.sqlite')
    cur = conn.cursor()
    data = {"id": "0001","write_api_key": "PYF7YMZNOM3TJVSM",}
    data['updates'] = []
    cur.execute('SELECT * FROM meter_table')
    for row in cur:
        data['updates'].append({
            "meterid": row[0],
            "energy": row[1],
            #"date": row[2],            #Original
            "date": 0,                  #Para el test
            "state": row[3]
            })
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    cur.close()
    return data
                

def update_date_base(meterid, data):
    pass

if __name__ == '__main__':
    print("Hello world")
    loras = [{"loraid":255,"slaves":[1,2,3]},{"loraid":254,"slaves":[0]}]
    energy_load(loras)
    load_json(id= "0001", write_api_key="PYF7YMZNOM3TJVSM")
    
    