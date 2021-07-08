'''
Created on Jul 7, 2021

@author: adrian
'''
import sqlite3

def energy_load(loras, needToDropTable = True):
    conn = sqlite3.connect('meter_db.sqlite')
    cur = conn.cursor()
    loras_id = ["00fe00","00ff01","00ff02","00ff03","00ff04"]
    if needToDropTable:
        cur.execute('DROP TABLE IF EXISTS meter_table')
        cur.execute('CREATE TABLE meter_table (meter_id TEXT, energy INTEGER, status BOOLEAN)')

    for lora in loras_id:
        cur.execute('INSERT INTO meter_table (meter_id, energy,status) VALUES (?, ?, ? )',(lora,0,True))
    conn.commit()
    cur.close()
    print(loras)

if __name__ == '__main__':
    print("Hello world")
    loras = [{"loraid":255,"slaves":[1,2,3]},{"loraid":254,"slaves":[0]}]
    energy_load(loras)