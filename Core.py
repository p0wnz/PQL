import json
from Crypto.Cipher import XOR
import pyminizip
import base64
import os
def encrypt(key, plaintext):
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))
def decrypt(key, ciphertext):
  cipher = XOR.new(key)
  return cipher.decrypt(base64.b64decode(ciphertext))
class DataBase:
    Tables=[]
    tab_name=[]
    name=""
    username=""
    password=""
    def __init__(self,name,username,password):
        self.name = name
        self.username = username
        self.password = password
    def verify_table(self,table):
        i=0
        for item in self.tab_name:
            if item == table:
                i+=1
        if i == 0:
            return 1
        else: return 0 
    def save_Database(self):
        path =os.getcwd()+ '/'+self.name
        if os.path.exists(os.getcwd()+self.name) ==False:
            os.mkdir(self.name)
        for table in self.Tables:
            self.save_table(table,self.password,self.name + '/'+table.name+".table") 
        self.save_id()
    def change_password(self,newPassword):
        self.password = newPassword
    def change_username(self,newUserName):
        self.username = newUserName
    def save_id(self):
        id = self.name+":"+self.username
        id = encrypt(self.password,id)
        filer = open(os.getcwd()+'/'+self.name+"/"+'Database.id','wr')
        filer.write(id)
        filer.close()
    def Table(self,Table_name):
        for i in range(0,len(self.tab_name)):
            if Table_name == self.tab_name[i]:
                return self.Tables[i]
        print "database not found"
    def get_Table_id(self,Table_name):
        for i in range(0,len(self.tab_name)):
            if Table_name == self.tab_name[i]:
                return i
        print "database not found"
    def load_id(self):
        try:
            filer = open(os.getcwd()+'/'+self.name+'/Database.id','r')
        except:
            print "invaild database name"
            return 1
        text =filer.read()
        try:
            text = decrypt(self.password,text)
            textAuth = text.split(":")
            pathh =os.getcwd()+'/'+self.name+'/'
            if textAuth[1] == self.username:
                files =os.listdir(os.getcwd()+'/'+self.name)
                files.remove('Database.id')
                for file in files:
                    self.load_table(self.password,pathh+file)
                    self.tab_name.append(file[:-6])
            else:
                print 'invaild username or passworD'
        except:
            print 'invaild usernamE or password'
            return 1
    def create_empty_Table(self,name):
        table =(Table({},[],[],[]))
        table.name= name
        self.Tables.append(table)
        self.tab_name.append(name)      
    def save_Table(self,table,password,File):
        with open(File, 'w') as outfile:
            json.dump([table.columns,table.col_name,table.keys,table.data_types], outfile)
            outfile.close()
        filer = open(File,'r')
        text =filer.read()
        filer.close()
        text = encrypt(password,text)
        filer = open(File,'wr')
        filer.truncate()
        filer.write(text)
        filer.close()
    def load_Table(self,password,File):
        filer = open(File,'r')
        text =filer.read()
        text = decrypt(password,text)
        data = json.loads(text)
        filer.close()
        self.Tables.append(Table(data[0],data[1],data[2],data[3]))
    def rename_Table(self,Table,NewName):
        if Table in self.tab_name:
            index =self.tab_name.index(Table)
            backup =self.Tables[index]
            backup.name=NewName
            del self.Tables[index]
            self.Tables.insert(index,backup)
            for i in range(0,len(self.tab_name)):
                if self.tab_name[i] == Table:
                    self.tab_name[i] = NewName
            return 0
        else:
            return 1
    def copy_table(self,table,newTable):
        tableBack=self.Table(table)
        tableBack.name=newTable
        self.Tables.append(tableBack)
        self.tab_name.append(newTable)
    def copy_table_to(self,table,newTable,position):
        tableBack=self.Table(table)
        tableBack.name=newTable
        self.Tables.append(tableBack)
        self.tab_name.append(newTable)
    def move_table(self,table,position):
        if table in self.tab_name:
            self.tab_name.remove(table)
            self.tab_name.insert(position,table)
    def remove_Table(self,table):
        if table in self.tab_name:
            self.Tables.pop(self.get_Table_id(table))
            self.tab_name.remove(table)
            return 0
        else:
            return 1
    def rename_Database(self,newName):
        self.name = newName
    def copy_Table_empty(self,table,newTable):
        if self.verify_table(table) == 1:
            return 1           
        self.create_empty_Table(newTable)
        self.Table(newTable).col_name = self.Table(table).col_name
        self.Table(newTable).keys = self.Table(table).keys
        self.Table(newTable).data_types = self.Table(table).data_types
        for item in self.Table(table).col_name:
            self.Table(newTable).columns[item]=[]
class Table:
    name=""
    columns={}
    col_name=[]
    keys=[]
    restric=[]
    data_types=[]
    data_types_available=['int','float','string',u'unistring','bool','money','id']
    def __init__(self,columns,col_name,keys,data_types):
        self.columns = columns
        self.col_name = col_name
        self.keys = keys
        self.data_types = data_types
    def verify_restriction(self,column):
        if self.verify_data_int(column):
            if column <= len(self.col_name):
                if self.restric[column] !=(0,0):
                    return True
                else:
                    return False
            else:
                return 1
        elif self.verify_column(column):
            if self.restric[self.get_column_id(column)] != (0,0):
                return True
            else: return False
        
        else: return 1
    def add_record(self,data):
        pramaters = data.split(',')
        if len(pramaters)!= len(self.col_name):
            return 1
        i=0
        for pramater in pramaters:
            l =self.add_to_column(self.col_name[i],pramater)
            if l == 0:
                i+=1
                pass
            else:
                self.tranucate_columns()
                return 1
        return 0
    def move_cell_upOne(self,TheColumn,cell_number):
        return self.move_cell(TheColumn,cell_number,cell_number-1)
    def move_cell_downOne(self,TheColumn,cell_number):
        return self.move_cell(TheColumn,cell_number,cell_number+1)
    def move_record_downOne(self,RecordNumber):
        return self.move_record(RecordNumber,RecordNumber+1)
    def move_record_upOne(self,RecordNumber):
        return self.move_record(RecordNumber,RecordNumber-1)
    def move_column_leftOne(self,columnNumber):
        return self.move_column(columnNumber,column_number-1)
    def move_column_rightOne(self,columnNumber):
        return self.move_column(columnNumber,column_number+1)
    def get_record(self,number):
        results=""
        for column in self.col_name:
            if len( self.columns[column]) <number:
                return 1
            results+=self.columns[column][number]+","
        results = results[:-1]
        return results
    def add_column_key(self,column):
        if not self.verify_column:
            print "column not found"
            return 1
        if self.get_column_data_type(column)=='bool':
            print "bools are not allowed to be in keys"
            return 1
        if column in self.keys:
            print 'column already in key'
            return 1
        if self.get_record_length() > 0:
            self.verify_key_content(column)
        self.keys.append(column)
        return 0
    def remove_column_key(self,column):
        if not self.verify_column:
            return 1
        if column in self.keys:
            self.keys.remove(column)
            return 0
        else:
            print "column is not in the keys"
            return 1
    def remove_record(self,recordNum):
        for column in self.col_name:
            if len(self.columns[column]) <recordNum:
                print "number too big!!"
                return 1
            del self.columns[column][recordNum]
    def get_column_amount(self):
        return len(self.col_name)
    def clean_records(self):
        for i in range(0,self.get_record_length()):
            self.remove_record(0)
    def clean_columns(self):
        for i in range(0,self.get_column_amount()):
            self.remove_column(0)
    def tranucate_columns(self):
        minem =self.min()
        for column in self.col_name:
            while len(self.columns[column]) > minem:
                self.columns[column].pop()
    def min(self):
        minum = 1000
        for column in self.col_name:
            if len(self.columns[column]) < minum:
                minum = len(self.columns[column])
        return minum
    def create_Column(self,name,data_type):
        data_try=self.verify_data_type(data_type)
        if data_try[0] == (False,99999)[0]:
            print "Invaild Data Type"
            return 1
        if name in self.col_name:
            print "column with the same name already created"
            return 1
        self.columns[name]=[]
        self.data_types.append(data_type)
        self.col_name.append(name)
        if self.get_record_length() >0:
            data_toBe_filled=None
            if self.get_column_data_type(name) =='int' or self.get_column_data_type(name) =='0':
                data_toBe_filled="0"
            elif self.get_column_data_type(name) =='string' or self.get_column_data_type(name) =='2':
                data_toBe_filled="NULL"
            elif self.get_column_data_type(name) =='float' or self.get_column_data_type(name) =='1':
                data_toBe_filled="0.0"
            elif self.get_column_data_type(name) =='unistring' or self.get_column_data_type(name) =='3':
                data_toBe_filled=(u"UNI-NULL")
            elif self.get_column_data_type(name) =='bool' or self.get_column_data_type(name) =='4':
                data_toBe_filled='FALSE'
            elif self.get_column_data_type(name) =='money' or self.get_column_data_type(name) =='5':
                data_toBe_filled="$0.00"
            elif self.get_column_data_type(name) =='id' or self.get_column_data_type(name) =='6':
                data_toBe_filled="0"
            else:
                return 1
            for i in range(0,self.get_record_length()):
                self.add_to_column(name,data_toBe_filled)
        self.restric.append((0,0))
    def remove_column(self,column):
        if self.verify_data_int(column):
            if self.col_name[column] in self.keys:
                self.remove_column_key(col_name[column])
            del self.data_types[column]
            del self.columns[self.col_name[column]]
            del self.col_name[0]
            return 0
        elif self.verify_column(column):
            self.data_types.remove(self.get_column_data_type(column))
            del self.columns[column]
            self.col_name.remove(column)
            if column in self.keys:
                self.remove_column_key(column)
            return 0
        else:
            return 1
    def add_to_column(self,column,data_added):
        if self.verify_key(column) ==0:
            if self.verify_data_key(column,data_added)==1:
                return 1
        if self.get_column_data_type(column) == "invaild column":
            print "Invaild column"
            return 1
        data_type= self.get_column_data_type(column)
        if self.verify_data(data_added,self.get_column_data_type(column)):
            if data_type == 'bool' or data_type =='4':
                data_added = data_added.upper()
            if data_type == 'money' or data_type =='5':
                if data_added[0][0] =='$':
                    data_added = data_added[1:]
                data_added = str(round(float(data_added),2))
                if data_added[0][0]!="$":
                    data_added = "$"+data_added
            if data_type == 'id' or data_type =='6':
                if len(self.columns[column]) > 0:
                    self.columns[(column.lower())].append(str(int(self.columns[column][-1])+1))
                    return 0
            self.columns[(column.lower())].append(data_added)
            return 0
        if self.verify_restriction(column):
            self.verify_restriction_inData(column)
        else:
            print "Invaid data Type"
            return 1
    def verify_data_type(self,data_type):
        found=False
        for i in range(0,len(self.data_types_available)):
            if self.data_types_available[i] == data_type:
                found=True
                return found,i
        return found,99999
    def get_columns(self):
        return self.col_name
    def get_column_data(self,column):
        if self.verify_column(column):
            return self.columns[column.lower()]
        else: return "invail column"
    def get_column_data_type(self,column):
        if self.verify_column(column):
            for i in range(0,len(self.col_name)):
                if (column.lower()) == self.col_name[i]:
                    return self.data_types[i]
            print "Data Type Not Found!"
            return 99999
        else:
            print "invaild data Type"
            return 99999
    def verify_data(self,data,data_type):
        if (data_type == 0 ) or (data_type =='int'):
            return self.verify_data_int(data)
        if (data_type ==1) or (data_type=='float'):
            return self.verify_data_float(data)
        if (data_type==2) or (data_type=='string'):
            return self.verify_data_string(data)
        if (data_type==3) or (data_type==u'unistring'):
            return self.verify_data_string(data)
        if (data_type==4) or (data_type=='bool'):
            return self.verify_data_boolean(data)
        if (data_type ==5) or (data_type == 'money'):
            return self.verify_data_money(data)
        if (data_type==6) or (data_type=='id'):
            return self.verify_data_int(data)
    def verify_data_string(self,data):
        try:
            str(data)
            return True
        except:
            return False
    def verify_data_boolean(self,data):
        true =True
        false = False
        if data.lower() =='false' or data.lower() == 'true':
            return True
        else : False
    def verify_restricted_data(self,column,data):
        if self.verify_data_int(column):
            if column <= len(self.col_name):
                if self.verify_restriction(column):
                    if len(data) >self.restric[column][1]:
                        return 1
                    elif len(data) <self.restric[column][0]:
                        return 1
                    else:return 0
                else:
                    return 0
            else:return False
        elif self.verify_column(column):
            if self.verify_restriction(column):
                if len(data) > self.restric[self.get_column_id(column)][1]:
                    return 1
                elif len(data) < self.restric[self.get_column_id(column)][0]:
                    return 1
                else:return 0
            else: return False
        else: return False
    def verify_restriction_edited(self,column,data):
        i=0
        if self.verify_data_int(column):
            if column <= len(self.col_name):
                if not self.verify_restriction(column):
                    return False
                while len(data) >self.restric[column][1]:
                    data = data[:-1]
                while len(data) <self.restric[column][0]:
                    data += str(i)
                    i+=1
            else:
                return 1
        elif self.verify_column(column):
            if not self.verify_restriction(column):
                return False
            while  len(data) > self.restric[self.get_column_id(column)][1]:
                data = data[:-1]
            while  len(data) < self.restric[self.get_column_id(column)][0]:
                data += str(i)
                i+=1
        else: return False
        return data
    def add_restriction(self,column,double):
        if self.verify_data_int(column):
            if column <= len(self.col_name):
                if self.verify_restriction(column):
                    return False
                self.restric[column] = double
                self.verify_restriction_inData(column)
                return 0
            else:
                return 1
        elif self.verify_column(column):
            if self.verify_restriction(column):
                return False
            self.restric[self.get_column_id(column)] = double
            self.verify_restriction_inData(column)
            return 0
        else: return False
    def verify_data_money(self,data):
        if data[0][0] =='$':
            data = data[1:]
        try:
            float(data)
            return True
        except:
            return False
    def verify_data_int(self,data):
        try:
            int(data)
            return True
        except:
            return False
    def verify_data_float(self,data):
        try:
            float(data)
            return True
        except:
            return False
    def get_record_length(self):
        if len(self.col_name) ==0:
            return False
        return len(self.columns[self.col_name[0]])
    def get_records(self):
        result_list=""
        x=self.get_record_length()
        for i in range(0,x):
            result_list+=self.get_record(i)+"\n"
        result_list = result_list[:-1]
        return result_list
    def verify_column(self,column):
        for i in range(0,len(self.col_name)):
            if column.lower() == self.col_name[i]:
                return True
        return False
    def verify_key(self,column):
        if column in self.keys:
            return 0
        else:
            return 1
    def verify_key_content(self,column):
        for i in range(0,self.get_record_length()):
            x=1
            repeated=0
            for y in range(0,self.get_record_length()):
                if self.columns[column][i] ==self.columns[column][y]:
                    repeated+=1
                    if repeated >1:
                        self.columns[column][y] = self.columns[column][y]+str(x)
                        repeated-=1
                        x+=1
    def verify_key_List(self,lisd):
        for i in range(0,self.get_record_length()):
            x=1
            repeated=0
            for y in range(0,self.get_record_length()):
                if lisd[i] ==lisd[y]:
                    repeated+=1
                    if repeated >1:
                        lisd[y] = lisd[y]+str(x)
                        repeated-=1
                        x+=1
    def verify_data_key(self,column,data):
        if data in self.columns[column]:
            print "its already there " + data +' in column '+ column
            return 1
        else:return 0
    def get_keys(self):
        return self.keys
    def update_cell(self,column,row,data):
        if self.verify_restriction(column):
            data= self.verify_restriction_edited(column,data)
        if not self.verify_data_string(data):
            return 1
        if self.verify_data_int(column):
            if row <= self.get_record_length():
                self.columns[self.col_name[column]][row-1] =data#begins with one
                return 0
        elif self.verify_column(column):
            if row <= self.get_record_length():
                self.columns[column][row-1] =data#begins with one
                return 0
    def update_record(self,number,data):
        i=0
        for column in self.col_name:
            if len(self.columns[column]) <self.get_record_length():
                return 1
            pramaters = data.split(',')
            if len(pramaters)!= len(self.col_name):
                return 1
            self.columns[column][number] = pramaters[i]
            i+=1
            if self.verify_restriction(column):
                self.verify_restriction_inData(column)
    def update_column(self,column,data):
        if self.verify_column(column):
            if self.verify_key(column)==0:
                x=1
                for i in range(0,self.get_record_length()):
                    self.columns[column][i] = data+str(x)
                    x+=1
            else:
                for i in range(0,self.get_record_length()):
                    self.columns[column][i] = data
        if self.verify_restriction(column):
            self.verify_restriction_inData(column)
    def move_cell(self,column,cell_number,moveto):
        if self.verify_column(column):
            if cell_number < self.get_record_length():
                backup =self.columns[column][cell_number]
                del self.columns[column][cell_number]
                self.columns[column].insert(moveto,backup)
                return 0
            else:return 1
        else:return 1
    def get_cell_by_info(self,text):
        for colum in self.col_name:
            for item in range(0,self.get_record_length()):
                if text == self.columns[colum][item]:
                    return ((self.get_column_id(colum)),(item))
        return False
    def move_record(self,cell_number,moveto):
        for column in self.col_name:
            if self.move_cell(column,cell_number,moveto) ==1:
                return 1
        return 0
    def get_column_id(self,column):
        if self.verify_column(column):
            for i in range(0,len(self.col_name)):
                if column == self.col_name[i]:
                    return i
        else:return False
    def move_column(self,column_number,moveto):
        if column_number < len(self.col_name):
            if moveto < len(self.col_name):
                backup = (self.col_name[column_number],self.data_types[column_number])
                del self.col_name[column_number]
                del self.data_types[column_number]
                self.col_name.insert(moveto,backup[0])
                self.data_types.insert(moveto,backup[1])
                return 0
            else:return 1
        else:return 1
    def rename_column(self,column,NewName):
        if self.verify_column(column):
            backup =self.columns[column]
            del self.columns[column]
            self.columns[NewName] = backup
            for i in range(0,len(self.columns)):
                if self.col_name[i] == column:
                    self.col_name[i] = NewName
            return 0
        else:
            return 1
    def update_column_List(self,column,lisd):
        if self.verify_column(column):
            if len(lisd) == self.get_record_length():
                if self.verify_key(column)==0:
                    print lisd
                    self.verify_key_List(lisd)
                    x=0
                    for i in range(0,self.get_record_length()):
                        self.columns[column][i] = lisd[i]
                        x+=1
                else:
                    x=0
                    for i in range(0,self.get_record_length()):
                        self.columns[column][i] = lisd[i]
                        x+=1
        if self.verify_restriction(column):
            self.verify_restriction_inData(column)
    def copy_column_to(self,column,newColumn,position):
        if self.verify_column(column):
            self.create_Column(newColumn,self.data_types[self.get_column_id(column)])
            self.update_column_List(newColumn,self.columns[column])
            self.move_column(self.get_column_id(newColumn),position)
    def copy_column(self,column,newColumn):
        if self.verify_column(column):
            self.create_Column(newColumn,self.data_types[self.get_column_id(column)])
            self.update_column_List(newColumn,self.columns[column])
    def copy_record(self,record_number):
        record =self.get_record(record_number)
        self.add_record(record)
    def copy_record_to(self,record_number,position):
        record =self.get_record(record_number)
        self.add_record(record)
        self.move_record(self.get_record_length()-1,position)
    def copy_cell(self,cell,cell2):
        cellback =self.get_cell(cell[0],cell[1])
        self.update_cell(cell2[0],cell2[1]+1,cellback)
    def get_cell(self,row,column):
        if row > len(self.col_name) or column > self.get_record_length():
            return 1
        id = self.get_column_name(row)
        return self.columns[id][column]
    def get_column_name(self,number):
        if number < len(self.col_name):
            return self.col_name[number]
        return False
    def add_record_amount(self,record,amount):
        for i in range(0,amount):
            self.add_record(record)
    def get_record_by_data(self,record):
        for i in range(0,self.get_record_length()):
            result = ""
            for item in self.col_name:
                result += self.columns[item][i]+","
            result = result[:-1]
            if result == record:
                return i
        return False
    def verify_key_restricted(self,column):
        if (self.verify_key(column) and (self.verify_restriction(column))):
            return True
        else : return False
    def get_restricted_columns(self):
        list_Column=[]
        for i in range(0,self.get_column_amount()):
            if self.restric[i] !=(0,0):
                list_Column += self.col_name[i]
        return list_Column
    def change_restriction(self,column,double):
        if self.verify_data_int(column):
            if column <= len(self.col_name):
                if self.verify_restriction(column):
                    self.restric[column] =double
                    self.verify_restriction_inData(column)
                else: return False
            else:return False
        elif self.verify_column(column):
            if self.verify_restriction(column):
                self.restric[self.get_column_id(column)]=double
                self.verify_restriction_inData(column)
            else: return False
        else: return False
    def remove_restriction(self,column):
        if self.verify_data_int(column):
            if column <= len(self.col_name):
                if self.verify_restriction(column):
                    self.restric[column] =(0,0)
                else: return False
            else:return False
        elif self.verify_column(column):
            if self.verify_restriction(column):
                self.restric[self.get_column_id(column)]=(0,0)
            else: return False
        else: return False
    def verify_restriction_inData(self,column):
        if self.verify_data_int(column):
            if column <= len(self.col_name):
                if self.verify_restriction(column):
                    for i in range (0,self.get_record_length()):
                        self.columns[self.get_column_name(column)][i] = self.verify_restriction_edited(column,self.columns[self.get_column_name(column)][i]) 
                else: return False
            else:return False
        elif self.verify_column(column):
            if self.verify_restriction(column):
                for i in range (0,self.get_record_length()):
                    self.columns[column][i] = self.verify_restriction_edited(column,self.columns[column][i])
            else: return False
        else: return False
##########################################
db =DataBase('foreign','dodo','password')
db.create_empty_Table('Students')
print db.Tables
print db.tab_name
db.rename_Table("Students","stupids")
db.copy_table("stupids","morons")
print db.Tables
print db.tab_name
db.Tables[0].create_Column("name","string")
db.Tables[0].create_Column("grade","int")
db.Tables[0].add_record("aref,9")
db.Tables[0].add_record("aref,9")
db.Table("stupids").add_record("aref,9")
db.Tables[0].add_record("aref,9")
#db.Tables[0].add_column_key("name")
print db.Tables[0].columns
print db.Tables[0].col_name
db.Tables[0].update_column_List("name",["aref","aref","boorare","thoor"])
print db.Tables[0].columns
print db.Tables[0].col_name
db.Table("stupids").copy_cell((0,2),(0,0))
print db.Table('stupids').columns
print db.Table('stupids').data_types
print db.Table('stupids').col_name
db.Table
print "##########################################################################"
print db.verify_table("stupids")
db.copy_Table_empty("stupids","monsters")
print db.Table("monsters").columns
db.Table("stupids").clean_records()
#print db.Table("stupids").columns
#db.Table("stupids").clean_columns()
#print db.Table("stupids").columns
print db.Table("stupids").col_name
db.Table("stupids").add_record("Aref,88")
db.Table("stupids").add_record("fLS,28")
db.Table("stupids").add_record("momentom,18")
db.Table("stupids").add_record("boo,58")
db.Table("stupids").add_record("foo,528")
print db.Table("stupids").columns
print db.Table("stupids").get_cell_by_info("528")
print db.Table("stupids").get_record_by_data("boo,58")
print db.Table("stupids").restric
print db.Table("stupids").verify_restriction("name")
print db.Table("stupids").get_restricted_columns()
print "#################################################################################"
print db.Table("stupids").add_restriction("name",(8,9))
print db.Table("stupids").verify_restriction_edited("name","assholetoomany")
print db.Table("stupids").verify_restricted_data("name","assholeto")
print db.Table("stupids").restric
print db.Table("stupids").change_restriction("name",(0,4))
print db.Table("stupids").verify_restriction_inData("name")
print db.Table("stupids").columns
print db.Table("stupids").restric