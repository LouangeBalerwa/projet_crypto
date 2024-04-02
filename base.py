import mysql.connector


def connecter():

    db = mysql.connector.connect(
        host ='localhost',
        user = 'root',
        password='',
        database = 'etudiant'
    )
    
    return db
