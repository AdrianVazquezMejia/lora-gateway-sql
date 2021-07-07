'''
Created on Jul 7, 2021

@author: adrian
'''
import unittest
import sqlite3
from src.sqlite_manager import *
from multiprocessing import active_children
from sqlite_manager import energy_load

loras = [{"loraid":255,"slaves":[1,2,3]},{"loraid":254,"slaves":[0]}]

class Test(unittest.TestCase):        

    def testSerialMetersCreates(self):
        energy_load(loras)
        conn = sqlite3.connect('meter_db.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT meter_id FROM meter_table ORDER BY meter_id ASC')
        expected_meter_id = ["00fe00","00ff01","00ff02","00ff03","00ff04"]
        actual_meter_id = []
        for row in cur:
            actual_meter_id.append(row[0])
        cur.close()
        self.assertEqual(actual_meter_id, expected_meter_id, "Must be equal")
        
        
        
    def testDataBaseCreation(self):
        conn = sqlite3.connect('meter_db.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT name FROM sqlite_master WHERE type= ? AND name= ? ',('table','meter_table'))
        expected_relation_name  = "meter_table"
        actual_relation_name = cur.fetchone()[0]
        cur.close()
        self.assertEqual(expected_relation_name, actual_relation_name, "Table does not exists")

    def testNewMeterAdd(self):
        
        conn = sqlite3.connect("meter_db.sqlite") 
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS meter_table')

        energy_load(loras)
        cur.execute('SELECT * FROM meter_table WHERE meter_id = ?',("00fe00", ))
        actual_tuple = cur.fetchone()
        expected_tuple = ('00fe00', 0, 1)
        cur.close()
        self.assertEqual(actual_tuple, expected_tuple)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()