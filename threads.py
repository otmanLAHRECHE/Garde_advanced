import datetime
import sqlite3
import time
from calendar import monthrange

import PyQt5
from PyQt5.QtCore import QThread, pyqtSignal

from database_operations import load_workers, add_worker, update_worker, delete_worker, load_garde_month, \
    add_garde_month, check_month, delete_garde_month
from tools import get_workerId_by_name, get_workerService_by_name


class ThreadLoadingApp(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self):
        super(ThreadLoadingApp, self).__init__()

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(100):
            self._signal.emit(i)
            # time.sleep(0.1)
        self._signal_result.emit(True)


class ThreadLoadWorkers(QThread):
    _signal = pyqtSignal(int)
    _signal_list = pyqtSignal(list)
    _signal_result = pyqtSignal(bool)

    def __init__(self, service):
        super(ThreadLoadWorkers, self).__init__()
        self.service = service

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        workers = load_workers(self.service)
        index = 0
        for worker in workers:
            list = []
            list.append(index)
            list.append(worker)
            self._signal_list.emit(list)
            index = index + 1

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)


class ThreadAddWorker(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, service, name):
        super(ThreadAddWorker, self).__init__()
        self.service = service
        self.name = name

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        add_worker(self.name, self.service)

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)


class ThreadUpdateWorker(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, id, name):
        super(ThreadUpdateWorker, self).__init__()
        self.id = id
        self.name = name

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        update_worker(self.name, self.id)

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)


class ThreadDeleteWorker(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, id):
        super(ThreadDeleteWorker, self).__init__()
        self.id = id

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        delete_worker(self.id)

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)


class ThreadLoadGardeMonth(QThread):
    _signal = pyqtSignal(int)
    _signal_list = pyqtSignal(list)
    _signal_result = pyqtSignal(bool)

    def __init__(self, service):
        super(ThreadLoadGardeMonth, self).__init__()
        self.service = service

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        months = load_garde_month(self.service)
        index = 0
        for month in months:
            list = []
            list.append(index)
            list.append(month)
            self._signal_list.emit(list)
            index = index + 1

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)


class ThreadAddGardeMonth(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, service, m, y):
        super(ThreadAddGardeMonth, self).__init__()
        self.service = service
        self.m = m
        self.y = y

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        res = check_month(self.m, self.y, self.service)

        if res:
            count = res[0]
            if count[0] == 0:
                can_add = True
            else:
                can_add = False

        else:
            can_add = True

        if can_add:
            add_garde_month(self.m, self.y, self.service)
            for i in range(30, 99):
                self._signal.emit(i)

            self._signal_result.emit(True)
        else:
            for i in range(30, 99):
                self._signal.emit(i)

            self._signal_result.emit(False)


class ThreadDeleteGardeMonth(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, id):
        super(ThreadDeleteGardeMonth, self).__init__()
        self.id = id

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        for i in range(30):
            self._signal.emit(i)

        delete_garde_month(self.id)

        for i in range(30, 99):
            self._signal.emit(i)

        self._signal_result.emit(True)


class ThreadGuard(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(list)

    def __init__(self, service, num_days, month, year):
        super(ThreadGuard, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year
        self.service = service

        if self.service == "inf" or self.service == "radio" or self.service == "labo" or self.service == "admin" or self.service == "pharm" or self.service == "dentiste_inf":
            self.data = [("Jours", "Date", "De 08h:00 à 16h:00", "De 16h:00 à 08h:00")]
        else:
            self.data = [("Jours", "Date", "De 08h:00 à 20h:00", "De 20h:00 à 08h:00")]

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        for row in range(self.num_days):

            prog = row * 100 / self.num_days
            day = row + 1
            x = datetime.datetime(self.year, self.month, day)
            if self.service == "urgence" or self.service == "dentiste":
                light = "Dr/ "
                night = "Dr/ "
            else:
                light = ""
                night = ""
            m = ""
            if x.strftime("%A") == "Saturday":
                m = "Samedi"
            elif x.strftime("%A") == "Sunday":
                m = "Dimanche"
            elif x.strftime("%A") == "Monday":
                m = "Lundi"
            elif x.strftime("%A") == "Tuesday":
                m = "Mardi"
            elif x.strftime("%A") == "Wednesday":
                m = "Mercredi"
            elif x.strftime("%A") == "Thursday":
                m = "Jeudi"
            elif x.strftime("%A") == "Friday":
                m = "Vendredi"

            if self.month / 10 >= 1:
                if day / 10 >= 1:
                    date_day = str(day) + "/" + str(self.month) + "/" + str(self.year)
                else:
                    date_day = str(0) + str(day) + "/" + str(self.month) + "/" + str(self.year)
            else:
                if day / 10 >= 1:
                    date_day = str(day) + "/" + str(0) + str(self.month) + "/" + str(self.year)
                else:
                    date_day = str(0) + str(day) + "/" + str(0) + str(self.month) + "/" + str(self.year)

            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.periode =? and guard.d =? and guard.m =? and guard.y =?'
            cur.execute(sql_q, (self.service, 'light', day, self.month, self.year))
            results_light = cur.fetchall()

            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.periode =? and guard.d =? and guard.m =? and guard.y =?'
            cur.execute(sql_q, (self.service, 'night', day, self.month, self.year))
            results_night = cur.fetchall()


            if results_light:
                rl = results_light[0]
                light = light + str(rl[0])

            if results_night:
                rn = results_night[0]
                night = night + str(rn[0])

            data_day = (m, date_day, light, night)

            self.data.append(data_day)
            self._signal.emit(int(prog))
            time.sleep(0.1)

        connection.close()
        self._signal_result.emit(self.data)


class Thread_create_guard(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(bool)

    def __init__(self, service, num_days, month, year, table):
        super(Thread_create_guard, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year
        self.table = table
        self.service = service

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        for row in range(self.num_days):
            day = row + 1
            prog = row * 100 / self.num_days
            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.periode =? and guard.d =? and guard.m =? and guard.y =?'
            cur.execute(sql_q, (self.service, 'light', day, self.month, self.year))
            results_light = cur.fetchall()
            check = self.table.cellWidget(row, 2)
            med_name = check.chose.currentText()

            check_2 = self.table.cellWidget(row, 3)
            med_name_2 = check_2.chose.currentText()

            if results_light:

                rl = results_light[0]

                if str(rl[0]) == med_name:
                    print("do nothing")
                elif str(rl[0]) != med_name and med_name != "":
                    id1 = get_workerId_by_name(str(rl[0]), self.service)[0]
                    id_new = get_workerId_by_name(med_name, self.service)[0]
                    id1 = id1[0]
                    id_new = id_new[0]
                    sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'light', id1))

                    sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'light', id_new))

                elif str(rl[0]) != med_name and med_name == "":

                    id1 = get_workerId_by_name(str(rl[0]), self.service)[0]
                    id1 = id1[0]
                    sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'light', id1))

            elif med_name != "":
                id_new = get_workerId_by_name(med_name, self.service)[0]
                id_new = id_new[0]
                sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                cur.execute(sql_q_light, (day, self.month, self.year, 'light', id_new))

            # guard shift night :

            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.periode =? and guard.d =? and guard.m =? and guard.y =?'
            cur.execute(sql_q, (self.service, 'night', day, self.month, self.year))
            results_night = cur.fetchall()
            print(results_night)

            if results_night:
                rn = results_night[0]

                if str(rn[0]) == med_name_2:
                    print("do nothing")
                elif str(rn[0]) != med_name_2 and med_name_2 != "":
                    id1 = get_workerId_by_name(str(rn[0]), self.service)[0]
                    id_new = get_workerId_by_name(med_name_2, self.service)[0]
                    id1 = id1[0]
                    id_new = id_new[0]
                    sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'night', id1))

                    sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'night', id_new))

                elif str(rn[0]) != med_name_2 and med_name_2 == "":

                    id1 = get_workerId_by_name(str(rn[0]), self.service)[0]
                    id1 = id1[0]
                    sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'night', id1))

            elif med_name_2 != "":
                id_new = get_workerId_by_name(med_name_2, self.service)[0]
                id_new = id_new[0]
                sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                cur.execute(sql_q_light, (day, self.month, self.year, 'night', id_new))

            connection.commit()
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal.emit(True)


class Thread_load_guards(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(list)
    _signal_finish = pyqtSignal(bool)

    def __init__(self, service, num_days, month, year):
        super(Thread_load_guards, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year
        self.service = service

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        for row in range(self.num_days):
            day = row + 1
            prog = row * 100 / self.num_days


            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.periode =? and guard.d =? and guard.m =? and guard.y =?'
            cur.execute(sql_q, (self.service, 'light', day, self.month, self.year))
            results_light = cur.fetchall()

            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.periode =? and guard.d =? and guard.m =? and guard.y =?'
            cur.execute(sql_q, (self.service, 'night', day, self.month, self.year))
            results_night = cur.fetchall()

            list = []
            list.append(row)
            list.append(results_light)
            list.append(results_night)

            self._signal.emit(list)
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal_finish.emit(True)


class ThreadAutoGuard(QThread):
    _signal = pyqtSignal(list)
    _signal_status = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, num_days, month, year, service, table, auto):
        super(ThreadAutoGuard, self).__init__()
        self.month = month
        self.year = year
        self.service = service
        self.table = table
        self.num_days = num_days
        self.auto = auto

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        index_max = len(self.auto)
        index_max = index_max - 1
        index = 0

        for row in range(self.num_days):
            day = row + 1
            prog = row * 100 / self.num_days

            x = datetime.datetime(self.year, self.month, day)


            if x.strftime("%A") == "Saturday":
                results_light = self.auto[index]
                if index == index_max:
                    results_night = self.auto[0]
                    index = 0
                else:
                    results_night = self.auto[index + 1]
                    index = index + 1

            elif x.strftime("%A") == "Sunday":
                if self.service == "urgence" or self.service == "radio" or self.service == "surv" or self.service == "inf" or self.service == "labo":

                    results_light = self.auto[index]
                    if index == index_max:
                        results_night = self.auto[0]
                        index = 0
                    else:

                        results_night = self.auto[index + 1]
                        index = index + 1
                else:
                    results_light = " "
                    results_night = self.auto[index]

            elif x.strftime("%A") == "Monday":
                if self.service == "urgence" or self.service == "radio" or self.service == "surv" or self.service == "inf" or self.service == "labo":

                    results_light = self.auto[index]
                    if index == index_max:
                        results_night = self.auto[0]
                        index = 0
                    else:

                        results_night = self.auto[index + 1]
                        index = index + 1
                else:
                    results_light = " "
                    results_night = self.auto[index]
            elif x.strftime("%A") == "Tuesday":
                if self.service == "urgence" or self.service == "radio" or self.service == "surv" or self.service == "inf" or self.service == "labo":

                    results_light = self.auto[index]
                    if index == index_max:
                        results_night = self.auto[0]
                        index = 0
                    else:

                        results_night = self.auto[index + 1]
                        index = index + 1
                else:
                    results_light = " "
                    results_night = self.auto[index]
            elif x.strftime("%A") == "Wednesday":
                if self.service == "urgence" or self.service == "radio" or self.service == "surv" or self.service == "inf" or self.service == "labo":

                    results_light = self.auto[index]
                    if index == index_max:
                        results_night = self.auto[0]
                        index = 0
                    else:

                        results_night = self.auto[index + 1]
                        index = index + 1
                else:
                    results_light = " "
                    results_night = self.auto[index]
            elif x.strftime("%A") == "Thursday":
                if self.service == "urgence" or self.service == "radio" or self.service == "surv" or self.service == "inf" or self.service == "labo":

                    results_light = self.auto[index]
                    if index == index_max:
                        results_night = self.auto[0]
                        index = 0
                    else:

                        results_night = self.auto[index + 1]
                        index = index + 1
                else:
                    results_light = " "
                    results_night = self.auto[index]
            elif x.strftime("%A") == "Friday":
                results_light = self.auto[index]
                if index == index_max:
                    results_night = self.auto[0]
                    index = 0
                else:
                    results_night = self.auto[index + 1]
                    index = index + 1

            if index == index_max:
                index = 0
            else:
                index = index + 1
            list = []
            list.append(row)
            list.append(results_light)
            list.append(results_night)

            self._signal.emit(list)
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        self._signal_result.emit(True)


class Thread_recap_load(QThread):
    _signal_status = pyqtSignal(int)
    _signal_users = pyqtSignal(list)
    _signal = pyqtSignal(list)
    _signal_finish = pyqtSignal(bool)

    def __init__(self, month, year, service):
        super(Thread_recap_load, self).__init__()
        self.service = service
        self.month = month
        self.year = year

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        sql_q = 'SELECT DISTINCT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.m =? and guard.y =?'
        cur.execute(sql_q, (self.service, self.month, self.year))

        res = cur.fetchall()
        self.agents = res
        self._signal_users.emit(self.agents)
        self.num_days = monthrange(self.year, self.month)[1]
        pr = 0
        for agent in self.agents:

            jo = 0
            jw = 0
            jf = 0
            prog = pr * 100 / self.num_days

            if self.service == "urgence_surv_inf":
                serv = get_workerService_by_name(agent[0])
                serv = serv[0]
                id_ag = get_workerId_by_name(agent[0], serv[0])
                id_ag = id_ag[0]
            else:
                id_ag = get_workerId_by_name(agent[0], self.service)
                id_ag = id_ag[0]

            sql_q = 'SELECT recap.jo,recap.jw,recap.jf FROM recap INNER JOIN health_worker ON health_worker.worker_id = recap.agents_id where service=? and recap.agents_id =? and recap.m =? and recap.y =?'
            cur.execute(sql_q, (self.service, id_ag[0], self.month, self.year))

            res1 = cur.fetchall()

            if res1:
                res1 = res1[0]
                jo = res1[0]
                jw = res1[1]
                jf = res1[2]

            else:
                for day in range(self.num_days):
                    d = day + 1
                    x = datetime.datetime(self.year, self.month, d)
                    sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and health_worker.worker_id = ?  and guard.d =? and guard.m =? and guard.y =?'
                    cur.execute(sql_q, (self.service, id_ag[0], d, self.month, self.year))
                    result = cur.fetchall()

                    if result:
                        if x.strftime("%A") == "Saturday":
                            jw = jw + 1
                        elif x.strftime("%A") == "Sunday":
                            jo = jo + 1
                        elif x.strftime("%A") == "Monday":
                            jo = jo + 1
                        elif x.strftime("%A") == "Tuesday":
                            jo = jo + 1
                        elif x.strftime("%A") == "Wednesday":
                            jo = jo + 1
                        elif x.strftime("%A") == "Thursday":
                            jo = jo + 1
                        elif x.strftime("%A") == "Friday":
                            jw = jw + 1

            list = []
            list.append(agent[0])
            list.append(jo)
            list.append(jw)
            list.append(jf)
            list.append(pr)
            pr = pr + 1

            self._signal.emit(list)
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal_finish.emit(True)


class Thread_save_recap(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(bool)

    def __init__(self, month, year, table, service):
        super(Thread_save_recap, self).__init__()
        self.month = month
        self.year = year
        self.table = table
        self.service = service

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        for row in range(self.table.rowCount()):
            prog = row * 100 / self.table.rowCount()
            if type(self.table.item(row, 2)) == PyQt5.QtWidgets.QTableWidgetItem:
                id_agn = get_workerId_by_name(self.table.item(row, 1).text(), self.service)
                id_agn = id_agn[0]
                sql_q = 'SELECT recap.jo, recap.jw, recap.jf FROM recap INNER JOIN health_worker ON health_worker.worker_id = recap.agents_id where service=? and recap.agents_id =? and recap.m =? and recap.y =?'
                cur.execute(sql_q, (self.service, id_agn[0], self.month, self.year))

                results = cur.fetchall()

                jo2 = int(self.table.item(row, 2).text())
                jw2 = int(self.table.item(row, 3).text())
                jf2 = int(self.table.item(row, 4).text())

                if results:
                    results = results[0]
                    jo1 = results[0]
                    jw1 = results[1]
                    jf1 = results[2]

                    if jo1 == jo2 and jw1 == jw2 and jf1 == jf2:
                        print("do nothing")
                    else:
                        if jo1 != jo2:
                            sql_q = 'UPDATE recap SET jo =? where  recap.agents_id =? and recap.m =? and recap.y =?'
                            cur.execute(sql_q, (jo2, id_agn[0], self.month, self.year))
                        if jw1 != jw2:
                            sql_q = 'UPDATE recap SET jw =? where  recap.agents_id =? and recap.m =? and recap.y =?'
                            cur.execute(sql_q, (jw2, id_agn[0], self.month, self.year))
                        if jf1 != jf2:
                            sql_q = 'UPDATE recap SET jf =? where  recap.agents_id =? and recap.m =? and recap.y =?'
                            cur.execute(sql_q, (jf2, id_agn[0], self.month, self.year))

                else:
                    if jo2 == 0 and jw2 == 0 and jf2 == 0:
                        print("do nothing")
                    else:
                        sql_q = 'INSERT INTO recap (jo,jw,jf,m,y,agents_id) VALUES (?,?,?,?,?,?)'
                        cur.execute(sql_q, (jo2, jw2, jf2, self.month, self.year, id_agn[0]))

            connection.commit()
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal.emit(True)


class ThreadRecapExport(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(list)

    def __init__(self, month, year, service):
        super(ThreadRecapExport, self).__init__()
        self.service = service
        self.month = month
        self.year = year
        self.data = [(" / ", "Jours ouvrable", "Jours week-end", "Jours fériés", "Total")]

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        sql_q = 'SELECT DISTINCT  health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.m =? and guard.y =?'
        cur.execute(sql_q, (self.service, self.month, self.year))
        res = cur.fetchall()

        sql_q = 'SELECT DISTINCT  count(*) FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.m =? and guard.y =?'
        cur.execute(sql_q, (self.service, self.month, self.year))
        res2 = cur.fetchall()

        count = res2[0]
        row = 0
        for agent in res:
            prog = row * 100 / count[0]

            id_agn = get_workerId_by_name(agent[0], self.service)
            id_agn = id_agn[0]

            sql_q = 'SELECT recap.jo, recap.jw, recap.jf FROM recap INNER JOIN health_worker ON health_worker.worker_id = recap.agents_id where service=? and recap.agents_id =? and recap.m =? and recap.y =?'
            cur.execute(sql_q, (self.service, id_agn[0], self.month, self.year))

            results = cur.fetchall()
            if results:
                results = results[0]

                jo = results[0]
                jw = results[1]
                jf = results[2]
            else:
                jo = 0
                jw = 0
                jf = 0

            total = int(jo) + int(jw) + int(jf)

            data_agent = (agent[0], jo, jw, jf, total)

            self.data.append(data_agent)

            time.sleep(0.3)
            self._signal.emit(int(prog))
            row = row + 1

        connection.close()
        print(self.data)
        self._signal_result.emit(self.data)

