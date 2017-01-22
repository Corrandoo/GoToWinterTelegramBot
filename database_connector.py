import mysql.connector, config


cnx = mysql.connector.connect(user='a0086306_gotobot', password=config.mySQLPassword, host='ikuznetsov.xyz', database='a0086306_gotobot')
cursor = cnx.cursor()
add_user = ("INSERT INTO subscribers " "(id, first_name, last_name, username)" "VALUES (%(id)s, %(first_name)s, %(last_name)s, %(username)s)")

def add_new_user_to_database(id, first_name, last_name, username):
    cnx = mysql.connector.connect(user='a0086306_gotobot', password=config.mySQLPassword, host='ikuznetsov.xyz',
                                  database='a0086306_gotobot')
    cursor = cnx.cursor()
    user = {
        'id': id, 'first_name': first_name, 'last_name': last_name, 'username': username
    }
    try:
        cursor.execute(add_user, user)
        cnx.commit()
    except mysql.connector.errors.IntegrityError:
        return "UniqueError"
def remove_user_from_database(id):
    cnx = mysql.connector.connect(user='a0086306_gotobot', password=config.mySQLPassword, host='ikuznetsov.xyz',
                                  database='a0086306_gotobot')
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM subscribers WHERE id=" + str(id))
    cnx.commit()
def search_user_in_database(id): # this method returns info about one user and gets its id
    cnx = mysql.connector.connect(user='a0086306_gotobot', password=config.mySQLPassword, host='ikuznetsov.xyz',
                                  database='a0086306_gotobot')
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM subscribers WHERE id="+str(id))
    result = cursor.fetchone()
    return result
def get_all_database(): # this method returns list of lists which contains info about every user
    cnx = mysql.connector.connect(user='a0086306_gotobot', password=config.mySQLPassword, host='ikuznetsov.xyz',
                                  database='a0086306_gotobot')
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM subscribers")
    result = cursor.fetchall()
    return result