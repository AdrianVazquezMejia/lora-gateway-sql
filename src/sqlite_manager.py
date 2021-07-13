'''
Created on Jul 7, 2021

@author: adrian
'''
import sqlite3
import datetime

def energy_load(loras):
    conn = sqlite3.connect('meter_db.sqlite')
    
    cur = conn.cursor()
    #cur.execute('DROP TABLE IF EXISTS meter_table ')  # Para pruebas
    cur.execute("CREATE TABLE IF NOT EXISTS meter_table (meter_id TEXT,energy INTEGER,date TEXT, status BOOLEAM)")
    conn.commit()
    for lora in loras:
        
        msb_4 = (lora["loraid"]).to_bytes(2,'big')

        for slave in lora['slaves']:
            lsb_2 = (slave).to_bytes(1,'big')
            meter_id = msb_4+lsb_2
            cur.execute('SELECT * FROM meter_table WHERE meter_id = ?',(meter_id.hex(), ))
            if cur.fetchone() == None:
                date = datetime.datetime.now()
                #cur.execute("INSERT INTO meter_table (meter_id, energy, date, status) VALUES(?,?,?,?)",(meter_id.hex(),0,date,False))      #Original
                cur.execute("INSERT INTO meter_table(meter_id,energy,status) VALUES(?,?,?)",(meter_id.hex(),0,1))      #Modificado para el test
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
            "date": row[2],
            "state": row[3]
            })
    cur.close()
    return data
                
def update_date_base(meterid, data):
    time = datetime.datetime.now()
    conn = sqlite3.connect('meter_db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT meter_id FROM meter_table WHERE meter_id = ?', (meterid,) )
    isInDataBase = cur.fetchall()
    if isInDataBase:
        cur.execute('UPDATE meter_table SET energy = ?, date = ? ',(data,time, ))
        conn.commit()
        cur.close()
        return 0 
    else:
        cur.close()
        return -1

    
if __name__ == '__main__':
    print("Hello world")
    loras = [{"loraid":255,"slaves":[1,2,3,4]},{"loraid":254,"slaves":[0]}]
    energy_load(loras)
    return_json =load_json(id= "0001", write_api_key="PYF7YMZNOM3TJVSM")
    print(return_json)
    for i in range(len(return_json['updates'])):
        data = 1234
        return_update_date_base = update_date_base(return_json['updates'][i]['meterid'], data)
        

    
    