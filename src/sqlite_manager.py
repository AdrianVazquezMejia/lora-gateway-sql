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
    #cur.execute('DROP TABLE IF EXISTS meter_table ')#El objetivo de la base de dato es almacenar no se puede borrar
    #cur.execute("CREATE TABLE meter_table (meter_id STRING, energy INTEGER, date TEXT, state BOOLEAN)")   #Para el test
    conn.commit()
    #lsb en nombres mas human readable
    for lora in loras:# Prueba de esta manera
        
        msb_4 = (lora["loraid"]).to_bytes(2,'big')

        for slave in lora['slaves']:
            lsb_2 = (slave).to_bytes(1,'big')
            meter_id = msb_4+lsb_2
            #print(meter_id.hex()) # Mira como ya se imprime
            cur.execute('SELECT * FROM meter_table WHERE meter_id = ?',(meter_id.hex(), ))
            if cur.fetchone() == None:
                date = datetime.datetime.now()
                cur.execute("INSERT INTO meter_table(meter_id,energy,date,state) VALUES(?,?,?,?)",(meter_id.hex(),0,date,1))      #Modificado para el test
            conn.commit() 
    cur.close()


def load_json(id, write_api_key):
    conn = sqlite3.connect('meter_db.sqlite')
    cur = conn.cursor()
    data = {"id": id,"write_api_key": write_api_key,}
    data['updates'] = []
    cur.execute('SELECT * FROM meter_table')
    for row in cur:
        data['updates'].append({
            "meterid": row[0],
            "energy": row[1],
            "date": row[2],            #Original
            #"date": 0,                  #Para el test
            "state": row[3]
            })
    cur.close()
    return data
                

def update_date_base(meterid, data):
    pass

if __name__ == '__main__':
    print("Hello world")
    loras = [{"loraid":255,"slaves":[1,2,3,4]},{"loraid":254,"slaves":[0]}]
    energy_load(loras)
    return_json =load_json(id= "0001", write_api_key="PYF7YMZNOM3TJVSM")
    print(return_json)
    