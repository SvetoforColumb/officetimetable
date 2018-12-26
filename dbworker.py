import sqlite3

import config


def addUser(user_id, t_name, t_username):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("select tid from USERS where tid=" + str(user_id))
    result = cursor.fetchall()
    if not result:
        cursor.execute("insert into USERS (tid, name, username, state, remind_time) values ('" + str(user_id) + "', '" +
                       t_name + "', '" + t_username + "', 0,15)")
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


def setLastNode(user_id):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("select count(*) from reminders where owner_id=" + str(user_id))
    conn.commit()
    conn.close()
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    num = cursor.fetchall()
    cursor.execute("update USERS set last_note_id='" + str(num) + "' where tid=" + str(user_id))
    conn.commit()
    conn.close()


def getLastNoteId(user_id):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("select last_note_id from USERS where tid=" + str(user_id))
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
        cursor.execute("insert into reminders (owner_id, text, remind_date, remind_time) values (" + str(user_id)
                       + ", " + text + ", '0', '0')")
    cursor.execute("update USERS set state=0 where tid=" + str(user_id))
    conn.commit()
    conn.close()
    setLastNode(user_id)


def setDate(user_id, value):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    lni = getLastNoteId(user_id)
    print(lni)
    cursor.execute('update reminders set "remind_date"=' + str(value) + " where id=" + str(lni))
    conn.commit()
    conn.close()


def setTime(user_id, value):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    lni = getLastNoteId(user_id)
    cursor.execute("update reminders set remind_time='" + str(value) + "' where id=" + str(lni))
    conn.commit()
    conn.close()


def setState(user_id, value):
    conn = sqlite3.connect(config.db_file)
    cursor = conn.cursor()
    cursor.execute("update USERS set state='" + str(value) + "' where tid=" + str(user_id))
    conn.commit()
    conn.close()



