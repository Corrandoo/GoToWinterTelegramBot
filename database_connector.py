import mysql.connector, config

cnx = mysql.connector.connect(user='a0086306_gotobot', password=config.mySQLPassword, host='ikuznetsov.xyz', database='a0086306_gotobot')
cursor = cnx.cursor()
add_user = ("INSERT INTO subscribers " "(id, first_name, last_name, username)" "VALUES (%(id)s, %(first_name)s, %(last_name)s, %(username)s)")
#query = ("SELECT id, first_name, last_name, username FROM subscribers " "WHERE id=" + 1111)

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
def search_user_in_database(id):
    result = cursor.execute("SELECT id, first_name, last_name, username FROM subscribers WHERE id=1111")
    print(result)

search_user_in_database(1111)
