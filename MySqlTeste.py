import mysql.connector
from mysql.connector import errorcode

db = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd="cockandballs",
)

db_name = "pi"
cursor = db.cursor()

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {};".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(db_name))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(db_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(db_name))
        db.database = db_name

TABLES = {}

TABLES['pessoa'] = ("CREATE TABLE Pessoa(idPessoa int AUTO_INCREMENT primary key, nome varchar(50), idade varchar(3))")
TABLES['salario'] = ("CREATE TABLE Salario(idPessoa int, foreign key(idPessoa) references Pessoa(idPessoa), salario float)")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

add_Pessoa = "INSERT INTO Pessoa (nome, idade) VALUES(%s, %s);"
data_Pessoa = ("Vini", 18)

add_Salario = "INSERT INTO Salario (idPessoa, salario) VALUES(%s, %s);"
data_salario = (1, 1500)

cursor.execute(add_Pessoa, data_Pessoa)
cursor.execute(add_Salario, data_salario)

db.commit()