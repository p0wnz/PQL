from Core import *
import time
class Selection:
    dataBase=None
    table=None
def greeting():
    print "IN THE NAME OF GOD"
    print "welcome to APB"
    print "made in 2016"
running=True
def list_commands(parameters):
    if  len(parameters)==1 or parameters[1].lower() == "help":
        list_help()
    if  len(parameters)==2 and parameters[1].lower() == "databases":
        list_DataBase()
def select_help():
    print "Select dataBase <dataBase Name> - Selects database"
    print "Select Table <table name> - "
def list_help():
    print "List dataBases -Lists all dataBases."
    print "List Columns -List All Tables in dataBase"
    print "List Columns -Lists all Columns in table."
    print "List Column Data <Column Name> -Lists data in Column."
    print "List Column type <Column Name> - Lists data type of Column."
    print "List Keys -Lists all Columns that have keys."
    print "List Records -Lists all Records."
    print "List Help - shows this menu."
    print "List Record height - show the length of the table"
def new_help():
    print "New Table <Table Name> -Brand new Table."
    print "New Column <Column Name> <Data type> -Brand new Column."
    print "New Record <record values> - Insert new Record."
    print "New Column key <Column Name> - Add column to key list"
def update_help():
    print "update Cell <column-number> <row> -Changes the value of a single cell."
    print "update Record <column> <record number> - Change values in record."
    print "update column <column> <data>- Replaces all data within column with the listed data."
def move_help():
    print "Move Cell <position> <new position> - Move cell within column"
    print "Move Record <position> <new position> - Move cell within Table"
    print "Move Column <position> <new position> - Move column within Table"
def list_DataBase():
    databases=[ name for name in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), name)) ]
    for i in databases:
        print i

def point_mark():
    global running
    results=raw_input(">>")
    if ';' in results:
        new_result = results.split(";")
        for result in new_result:
            interpreter(result)
    else:
        interpreter(results)
def interpreter(results):
    if results.lower() =="quit" or results.lower() =="end" or results.lower() =="exit" or results.lower() =="close":
        return False
    parameters = results.split(" ")
    if parameters[0].lower() == 'list':
       list_commands(parameters)
    return parameters
greeting()
while running:
    point_mark()
print "closing Right Now!!"
time.sleep(1)
quit()