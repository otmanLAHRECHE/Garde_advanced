import sqlite3


def load_workers(service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT * FROM health_worker where service=?'
    cur.execute(sql_q, (service,))
    results = cur.fetchall()
    connection.close()
    return results


def add_worker(name, service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
    med = (name, service)
    cur.execute(sql_q, med)
    connection.commit()
    connection.close()


def update_worker(name, id):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'UPDATE health_worker SET full_name= ? WHERE worker_id= ?'
    cur.execute(sql_q, (name, id))
    connection.commit()
    connection.close()


def delete_worker(id):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'DELETE FROM health_worker WHERE worker_id=?'
    cur.execute(sql_q, (id,))
    connection.commit()
    connection.close()


def load_garde_month(service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT * FROM guard_mounth where service=? ORDER BY m ASC'
    cur.execute(sql_q, (service,))
    results = cur.fetchall()
    connection.close()
    return results

def add_garde_month(month, year, service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = "INSERT INTO guard_mounth (m,y,service) values (?,?,?)"
    guard = (month, year, service)
    cur.execute(sql_q, guard)
    connection.commit()

def check_month(month, year, service):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT count(*) FROM guard_mounth where guard_mounth.m =? and guard_mounth.y =? and guard_mounth.service =? '
    cur.execute(sql_q, (month, year, service))
    res = cur.fetchall()
    connection.close()
    return res


def delete_garde_month(id):
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'DELETE FROM guard_mounth WHERE guard_mounth_id=?'
    cur.execute(sql_q, (id,))
    connection.commit()
    connection.close()

def load_groupes_inf():
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT health_worker.worker_id, health_worker.full_name, health_worker.service, groupe.g  FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id where health_worker.service=?'
    cur.execute(sql_q, ('inf',))
    results = cur.fetchall()
    connection.close()
    return results

def load_groupes_surv():
    connection = sqlite3.connect("database/sqlite.db")
    cur = connection.cursor()
    sql_q = 'SELECT health_worker.worker_id, health_worker.full_name, health_worker.service, groupe_surv.g  FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id where health_worker.service=?'
    cur.execute(sql_q, ('surv',))
    results = cur.fetchall()
    connection.close()
    return results
