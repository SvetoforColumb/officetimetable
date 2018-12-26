import sqlite3

import config


def addUser(user_id, name, username):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("select tid from USERS where tid=" + str(user_id))
    result = cursor.fetchall()
    if not result:
        cursor.execute("insert into USERS (tid, name, username, state, remind_time) values (" + str(user_id) + ", " +
                       name + ", " + username + ", '0','15')")
    cursor.execute("update USERS set state=0 where tid=" + str(user_id))
    conn.commit()
    conn.close()


def getState(user_id):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("select state from USERS where tid=" + str(user_id))
    result = cursor.fetchone()
    if not result:
        return "0"
    conn.commit()
    conn.close()
    return result


def addNote(user_id, text):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("select tid from USERS where tid=" + str(user_id))
    result = cursor.fetchall()
    if not result:
        cursor.execute("insert into reminders (owner_id, text) values (" + str(user_id)
                       + ", " + text + ")")
    cursor.execute("update USERS set state=0 where tid=" + str(user_id))
    conn.commit()
    conn.close()



def setState(user_id, value):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("update USERS set state='" + str(value) + "' where tid=" + str(user_id))
    conn.commit()
    conn.close()



