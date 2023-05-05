import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd="cockandballs",
    database="teste"
)

mycursor = db.cursor()

mycursor.execute("INSERT INTO Pessoa (nome, idade) VALUES (%s,%s)", ("Vini", 19))
db.commit()
# for x in mycursor:
#     print(x)