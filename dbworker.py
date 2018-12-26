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




