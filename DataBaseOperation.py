import mysql.connector
import json
from datetime import datetime

class DBOperation():

    def __init__(self):
        # We have below explicitly given db username and password
        # self.mydb = mysql.connector.connect(host='localhost',user='vehicle_user',passwd = 'vehicle_password',
        #                                   database = 'vehicle_parking_miniproject')
        #Now we read username or password from json file
        file = open('./config.json', 'r')
        dataic = json.loads(file.read())
        file.close()
        self.mydb = mysql.connector.connect(host='localhost', user=dataic['username'], passwd=dataic['password'],
                                            database=dataic['database'])

    def createTables(self):
        # This function is used to create a table and datatypes to fields to it
        cursor = self.mydb.cursor()
        #print('creating table')
        cursor.execute("DROP TABLE if exists admin")
        cursor.execute("DROP TABLE if exists customer")
        cursor.execute("DROP TABLE if exists vehicles")
        cursor.execute("DROP TABLE if exists Bigger_vehicles_lane_2")
        cursor.execute("DROP TABLE if exists Smaller_vehicles_lane_1")
        #print('after dropping tables')

        cursor.execute("CREATE TABLE admin (id int(255) AUTO_INCREMENT PRIMARY KEY,username varchar(30),password varchar(30))")
        cursor.execute("create table customer(cusid int AUTO_INCREMENT PRIMARY KEY,name varchar(30),mobile varchar(30),vehicle_type varchar(30))")
        cursor.execute("CREATE TABLE vehicles (cusid int references customer(cusid) ON delete cascade,vehicle_no varchar(30),entry_time varchar(30) not null,exit_time varchar(30) not null,is_exit varchar(30) not null,created_at varchar(30),updated_at varchar(30),primary key(cusid,vehicle_no))")
        cursor.execute("CREATE TABLE Smaller_vehicles_lane_1 (cusid int REFERENCES customer(cusid) ON DELETE CASCADE,vehicle_no varchar(30)  references vehicles(vehicle_no) on delete cascade,slot_two_id int auto_increment primary key,is_empty int)")
        cursor.execute("CREATE TABLE Bigger_vehicles_lane_2 (cusid int references customer(cusid) ON delete cascade,vehicle_no varchar(30)  references vehicles(vehicle_no) on delete cascade,slot_four_id int auto_increment primary key,is_empty int)")
        #print("table created")
        cursor.close()

    def InsertOneTimeData(self,space_two_wheeler,space_four_wheeler):
        # this function is used to create one time database entry for number of slots in parking lot
        #print("in admin ontime data")
        cursor = self.mydb.cursor()
        for x in range(space_two_wheeler):
            cursor.execute("INSERT into Smaller_vehicles_lane_1 (is_empty) values ('1')")
            self.mydb.commit()

        for x in range(space_four_wheeler):
            cursor.execute("INSERT into Bigger_vehicles_lane_2 (is_empty) values ('1')")
            self.mydb.commit()
        #print("after admin ontime data")
        cursor.close()

    def InsertAdmin(self,username,password):
        #print("in insert admin data")
        cursor=self.mydb.cursor()
        val=(username,password)
        cursor.execute("INSERT into admin (username,password) values (%s,%s)", val)
        self.mydb.commit()
        #print("after insert admin  data")
        cursor.close()

    def doAdminLogin(self,username,passowrd):
        cursor = self.mydb.cursor()
        #print('in do admin login')
        cursor.execute("select * from admin where username='"+username+"' and password='"+passowrd+"'")
        data = cursor.fetchall()
        #print("data from admin")
        #print(data)
        cursor.close()
        if len(data)>0:
            return True
        else:
            return False

    def getslotspace(self,name):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM "+name)
        data = cursor.fetchall()
        cursor.close()
        return data

    def getcurrentvehicle(self):
        # this function is used to get vehicle details which are currently parked from database
        cursor = self.mydb.cursor()
        # If vehicle is parked in any slot then is_exit will be 0
        cursor.execute("SELECT * FROM unionview where is_exit = '0'")
        data = cursor.fetchall()

        print('In get current vehicle:')
        cursor.close()
        return data

    def getallvehicle(self):
        # this function is used to get all vehicle details which were parked from database
        cursor = self.mydb.cursor()
        # If vehicle is parked in any slot then is_exit will be 0
        cursor.execute("SELECT * FROM customerhistory where is_exit = '1'")
        data = cursor.fetchall()
        cursor.close()
        return data

    def add_vehicles_database_two(self, name, vehicle_no, mobile_no, vehicle_type,slot_name):
        spaceid = self.spaceavailable(slot_name)
        if spaceid:
            print("in add_vehicle_database")
            current_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_customer = (name, mobile_no, vehicle_type)
            cursor = self.mydb.cursor()
            cursor.execute("INSERT into customer (name,mobile,vehicle_type) values (%s,%s,%s)",data_customer)
            self.mydb.commit()
            lastid=cursor.lastrowid
            print(id)
            data_vehicle = (lastid,vehicle_no,str(current_data), '',0,str(current_data), str(current_data))
            cursor.execute("INSERT into vehicles(cusid,vehicle_no,entry_time,exit_time,is_exit,created_at,updated_at) values (%s,%s,%s,%s,%s,%s,%s)",data_vehicle)
            self.mydb.commit()
            cursor.execute("UPDATE "+ slot_name +" set is_empty='0',cusid ='"+str(lastid)+"',vehicle_no ='"+vehicle_no+"'  where slot_two_id='"+str(spaceid)+"'")
            self.mydb.commit()
            cursor.close()
            return True
        else:
            return "No space available for parking"

    def add_vehicles_database_four(self, name, vehicle_no, mobile_no, vehicle_type,slot_name):
        spaceid = self.spaceavailable(slot_name)
        if spaceid:
            print("in add_vehicle_database")
            current_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_customer = (name, mobile_no,vehicle_type)
            cursor = self.mydb.cursor()
            cursor.execute("INSERT into customer (name,mobile,vehicle_type) values (%s,%s,%s)",data_customer)
            self.mydb.commit()
            lastid=cursor.lastrowid
            print(id)
            data_vehicle = (lastid,vehicle_no,str(current_data), '',0,str(current_data), str(current_data))
            cursor.execute("INSERT into vehicles(cusid,vehicle_no,entry_time,exit_time,is_exit,created_at,updated_at) values (%s,%s,%s,%s,%s,%s,%s)",data_vehicle)
            self.mydb.commit()
            cursor.execute("UPDATE "+ slot_name +" set is_empty='0',cusid ='"+str(lastid)+"',vehicle_no = '"+vehicle_no+"' where slot_four_id='"+str(spaceid)+"'")
            self.mydb.commit()
            cursor.close()
            return True
        else:
            return "No space available for parking"


    def spaceavailable(self,slot_name):
        cursor = self.mydb.cursor()

        cursor.execute("select * from "+slot_name+" where  is_empty = '1'")
        data = cursor.fetchall()

        if len(data)>0:
            # because slot id is in tuple we are acessing 1st element of tuple
            cursor.close()
            return data[0][2]
        else:
            cursor.close()
            return False

    def exitVehicle(self,id,vtype):
        cursor = self.mydb.cursor()
        current_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(vtype)
        if vtype == '2':
            print("after comparison")
            print(vtype)
            cursor.execute("UPDATE Smaller_vehicles_lane_1 set is_empty='1', cusid=NULL,vehicle_no = NULL where cusid='"+id+"'")
            self.mydb.commit()
        else:
            print("after comparison")
            print(vtype)
            cursor.execute("UPDATE Bigger_vehicles_lane_2 set is_empty='1', cusid=NULL,vehicle_no = NULL where cusid='"+id+"'")
            self.mydb.commit()

        cursor.execute("UPDATE vehicles set is_exit ='1', exit_time ='"+current_data+"' where cusid ='"+id+"'")
#       cursor.execute("UPDATE vehicles set is_exit = '1', exit_time ='"+current_data+"' where id='" + id + "'")
        self.mydb.commit()
        cursor.close()

    def remove_vehicles_database(self, vehicle_no, table_name):
        try:
            print("in remove_vehicle_database")
            cursor = self.mydb.cursor()
            cursor.execute("select * from vehicles where vehicle_no='" + vehicle_no + "'")
            data = cursor.fetchall()
            cursor.execute("delete from " + table_name + " where cusid ='" + str(data[0][0])+ "'")
            self.mydb.commit()
            cursor.close()
            return True
        except:
            print("Unable to delete vehicles record")
            self.mydb.rollback()
            return False

    def remove_customers_database(self, name, mobile_no, vehicle_type, table_name):
        try:
            print("in remove customer database")
            cursor = self.mydb.cursor()
            cursor.execute(
                "select * from customer where name='" + name + "' and mobile='" + mobile_no + "'  and vehicle_type='" + vehicle_type + "';")
            data = cursor.fetchall()
            print(data)
            cursor.execute("delete from " + table_name + " where cusid ='" + str(data[0][0]) + "'")
            self.mydb.commit()
            cursor.close()
            return True
        except :
            print("Unable to delete customer record")
            self.mydb.rollback()
            return False

    def RemoveAdmin(self,username,password):
        #print("in insert admin data")
        cursor=self.mydb.cursor()
        try:
            cursor.execute("select * from admin where username='" + username + "' and password='" + password + "'")
            data = cursor.fetchall()
            cursor.execute("delete from admin where id ='" + str(data[0][0]) + "'")
            self.mydb.commit()
            cursor.close()
            return True
        except:
            return False

        #print("after insert admin  data")


