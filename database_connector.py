import mysql.connector, config

cnx = mysql.connector.connect(user='a0086306_gotobot', password=config.mySQLPassword, host='ikuznetsov.xyz', database='a0086306_gotobot')
cursor = cnx.cursor()
add_user = ("INSERT INTO subscribers " "(id, first_name, last_name, username)" "VALUES (%(id)s, %(first_name)s, %(last_name)s, %(username)s)")


def add_new_user_to_database(id, first_name, last_name, username):
    user = {
        'id': id, 'first_name': first_name, 'last_name': last_name, 'username': username
    }
    cursor.execute(add_user, user)

    cnx.commit()
