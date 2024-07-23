
import pypyodbc as odbc
driver_name='SQL SERVER'
server = 'DESKTOP-ALUKKGH\SQLEXPRESS'
database = 'education_system'  

connection_string = f"""
DRIVER={{{driver_name}}};
SERVER={server};
DATABASE={database};
Trust Connection=yes;"""
def get_connection():
    try:
        connection = odbc.connect(connection_string)
        print("Connected to database successfully!")
        return connection
    except :
        print("Error connecting to database:")
        return None 

get_connection()