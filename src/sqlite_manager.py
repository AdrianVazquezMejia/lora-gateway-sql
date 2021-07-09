'''
Created on Jul 7, 2021

@author: adrian
'''
import sqlite3
import datetime

def energy_load(loras):
    #print("ENERGY LOAD INICIA")
    conn = sqlite3.connect('medidores.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS meter_db ')
    cur.execute("CREATE TABLE meter_db (meter_id STRING, energy INTEGER, date STRING, state INTEGER)")
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
            #print(loras[i]['slaves'][s])
            lsb_2 = str(0)+str(hex(loras[i]['slaves'][s]).split('x')[-1])
            meter_id = str('00'+msb_4+lsb_2)
            #print("METER_ID: ",meter_id)
            date = datetime.datetime.now()
            cur.execute('SELECT meter_id FROM meter_db')
            for row in cur:
                nuevo = 1
                #print("EL ROW ACTUAL",row[0])
                if(row[0] == meter_id): 
                    #print("Ya Existe",row[0],"en la base")
                    #print("ESTA ES",row[0])
                    nuevo = 0
                    break               
            if(nuevo==1):
#print("NUEVO MEDIDOR")
                cur.execute("INSERT INTO meter_db(meter_id,energy,date,state) VALUES(?,?,?,?)",(meter_id,0,date,0))
                conn.commit()
            nuevo = 1
    cur.close()


def load_json(id, write_api_key):
    return None


def update_date_base(meterid, data):
    pass

if __name__ == '__main__':
    print("Hello world")
    loras = [{"loraid":255,"slaves":[1,2,3]},{"loraid":254,"slaves":[0]}]
    energy_load(loras)
    #load_json(id= "0001", write_api_key="PYF7YMZNOM3TJVSM")
    
    