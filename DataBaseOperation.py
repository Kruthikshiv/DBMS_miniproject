import mysql.connector
import json
from datetime import datetime

class DBOperation():

    def __init__(self):
        # We have below explicitly given db username and password
        # self.mydb = mysql.connector.connect(host='localhost',user='vehicle_user',passwd = 'vehicle_password',
        #                                   database = 'vehicle_parking_miniproject')
        #Now we read username or password from json file
        file = open('./config.json','r')
        dataic = json.load(file.read())
        file.close()
        self.mydb = mysql.connector.connect(host='localhost', user=dataic['username'], passwd=dataic['password'],
                                            database=dataic['database'])

    def createTables(self):
        # This function is used to create a table and datatypes to fields to it
        cursor = self.mydb.cursor()
        cursor.execute("CREATE TABLE admin (id int(255) AUTO_INCREMENT PRIMARY KEY,username varchar(30),password varchar(30),created_at varchar(30))")
        cursor.execute("CREATE TABLE slots (id int(255) AUTO_INCREMENT PRIMARY KEY,vehicle_id varchar(30),space_for int(25),is_empty int(25))")
        cursor.execute("CREATE TABLE vehicles (id int(255) AUTO_INCREMENT PRIMARY KEY,name varchar(30),mobile varchar(30),entry_time varchar(30),exit_time varchar(30),is_exit varchar(30),vehicle_no varchar(30),vehicle_type varchar(30),created_at varchar(30),updated_at varchar(30))")
        cursor.close()

    def InsertOneTimeData(self,space_two_wheeler,space_four_wheeler):
        # this function is used to create one time database entry for number of slots in parking lot
        cursor = self.mydb.cursor()
        for x in range(space_two_wheeler):
            cursor.execute("INSERT into slots(space_for,is_empty) VALUES ('2','1')")
            self.mydb.commit()

        for x in range(space_four_wheeler):
            cursor.execute("INSERT into slots(space_for,is_empty) VALUES ('4','1')")
            self.mydb.commit()
        cursor.close()

    def InsertAdmin(self,username,password):
        cursor=self.mydb.cursor()
        val=(username,password)
        cursor.execute("INSERT into admin (username,password) values (%s,%s)",val)
        self.mydb.commit()
        cursor.close()