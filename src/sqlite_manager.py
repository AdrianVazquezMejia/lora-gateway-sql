'''
Created on Jul 7, 2021

@author: adrian
'''
import sqlite3
import datetime
# Doble comillas en vez de comillas simples
# nombres mas significativos para cur y conn i.e.: cur --> data_base_cursor
# Redefinicion de name 'data' de outer scope, osea 'data' esta en las funciones y en el main 
def energy_load(loras):
    
    conn = sqlite3.connect('meter_db.sqlite')
    cur = conn.cursor() 
    cur.execute("CREATE TABLE IF NOT EXISTS meter_table (meter_id TEXT,energy INTEGER,date TEXT, status BOOLEAM)")
    conn.commit()
    for lora in loras:
        
        msb_4 = (lora["loraid"]).to_bytes(2,'big')#nombres mas significativos a msb y lsb

        for slave in lora['slaves']:
            lsb_2 = (slave).to_bytes(1,'big')
            meter_id = msb_4+lsb_2
            cur.execute('SELECT * FROM meter_table WHERE meter_id = ?',(meter_id.hex(), ))
            if cur.fetchone() is None:
                date = datetime.datetime.now()
                cur.execute("INSERT INTO meter_table(meter_id,energy,date,status) VALUES(?,?,?,?)",(meter_id.hex(),0,date,1))
            conn.commit() 
    cur.close()


def load_json(id, write_api_key):
    conn = sqlite3.connect('meter_db.sqlite')
    cur = conn.cursor()
    data = {"id": id,"write_api_key": write_api_key,}# nombres mas significativos para data
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
    is_in_database = cur.fetchall()
    if is_in_database:
        cur.execute('UPDATE meter_table SET energy = ?, date = ? ',(data,time, ))
        conn.commit()
        cur.close()
        return 0 
    cur.close()
    return -1

    
if __name__ == '__main__':
    print("Hello world")
    loras = [{"loraid":255,"slaves":[1,2,3,4]},{"loraid":254,"slaves":[0]}]
    energy_load(loras)
    return_json =load_json(id= "0001", write_api_key="PYF7YMZNOM3TJVSM")
    print(return_json)
    for meter_serial in return_json['updates']:
        data = 3210
        return_update_date_base = update_date_base(meter_serial['meterid'], data)
        print(return_update_date_base)
    