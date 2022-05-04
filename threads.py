import datetime
import sqlite3
import time
from calendar import monthrange

import PyQt5
from PyQt5.QtCore import QThread, pyqtSignal

from database_operations import load_workers, add_worker, update_worker, delete_worker, load_garde_month, \
    add_garde_month, check_month, delete_garde_month, load_groupes_inf, load_groupes_surv
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


class Thread_state_load(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(list)
    _signal_finish = pyqtSignal(bool)

    def __init__(self, month, year):
        super(Thread_state_load, self).__init__()
        self.month = month
        self.year = year

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_homme where state_homme.m =? and state_homme.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_h = cur.fetchall()
        print("test")
        print(res_h)

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_famme where state_famme.m =? and state_famme.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_f = cur.fetchall()

        print(res_f)

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_enfant where state_enfant.m =? and state_enfant.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_e = cur.fetchall()

        print(res_e)

        self.Poumon = []
        self.OS = []
        self.Abdomen_simple = []
        self.UIV = []
        self.Cholecystographie = []
        self.Estomac = []
        self.Echographie = []
        self.Fibroscopie = []
        self.ECG = []

        if res_h:
            res_h = res_h[0]
            po = res_h[0]
            self.Poumon.append(po)
            os = res_h[1]
            self.OS.append(os)
            abd = res_h[2]
            self.Abdomen_simple.append(abd)
            uiv = res_h[3]
            self.UIV.append(uiv)
            chol = res_h[4]
            self.Cholecystographie.append(chol)
            est = res_h[5]
            self.Estomac.append(est)
            echo = res_h[6]
            self.Echographie.append(echo)
            fibr = res_h[7]
            self.Fibroscopie.append(fibr)
            ecg = res_h[8]
            self.ECG.append(ecg)
        else:
            self.Poumon.append(0)
            self.OS.append(0)
            self.Abdomen_simple.append(0)
            self.UIV.append(0)
            self.Cholecystographie.append(0)
            self.Estomac.append(0)
            self.Echographie.append(0)
            self.Fibroscopie.append(0)
            self.ECG.append(0)

        if res_f:
            res_f = res_f[0]
            po = res_f[0]
            self.Poumon.append(po)
            os = res_f[1]
            self.OS.append(os)
            abd = res_f[2]
            self.Abdomen_simple.append(abd)
            uiv = res_f[3]
            self.UIV.append(uiv)
            chol = res_f[4]
            self.Cholecystographie.append(chol)
            est = res_f[5]
            self.Estomac.append(est)
            echo = res_f[6]
            self.Echographie.append(echo)
            fibr = res_f[7]
            self.Fibroscopie.append(fibr)
            ecg = res_f[8]
            self.ECG.append(ecg)
        else:
            self.Poumon.append(0)
            self.OS.append(0)
            self.Abdomen_simple.append(0)
            self.UIV.append(0)
            self.Cholecystographie.append(0)
            self.Estomac.append(0)
            self.Echographie.append(0)
            self.Fibroscopie.append(0)
            self.ECG.append(0)

        if res_e:
            res_e = res_e[0]
            po = res_e[0]
            self.Poumon.append(po)
            os = res_e[1]
            self.OS.append(os)
            abd = res_e[2]
            self.Abdomen_simple.append(abd)
            uiv = res_e[3]
            self.UIV.append(uiv)
            chol = res_e[4]
            self.Cholecystographie.append(chol)
            est = res_e[5]
            self.Estomac.append(est)
            echo = res_e[6]
            self.Echographie.append(echo)
            fibr = res_e[7]
            self.Fibroscopie.append(fibr)
            ecg = res_e[8]
            self.ECG.append(ecg)
        else:
            self.Poumon.append(0)
            self.OS.append(0)
            self.Abdomen_simple.append(0)
            self.UIV.append(0)
            self.Cholecystographie.append(0)
            self.Estomac.append(0)
            self.Echographie.append(0)
            self.Fibroscopie.append(0)
            self.ECG.append(0)

        list = []
        list.append(self.Poumon)
        list.append(self.OS)
        list.append(self.Abdomen_simple)
        list.append(self.UIV)
        list.append(self.Cholecystographie)
        list.append(self.Estomac)
        list.append(self.Echographie)
        list.append(self.Fibroscopie)
        list.append(self.ECG)

        for prog in range(20):
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        print(list)
        self._signal.emit(list)

        connection.close()
        self._signal_finish.emit(True)


class Thread_save_state(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(bool)

    def __init__(self, month, year, table):
        super(Thread_save_state, self).__init__()
        self.month = month
        self.year = year
        self.table = table

        self.Poumon = []
        self.OS = []
        self.Abdomen_simple = []
        self.UIV = []
        self.Cholecystographie = []
        self.Estomac = []
        self.Echographie = []
        self.Fibroscopie = []
        self.ECG = []

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        for c in range(3):
            self.Poumon.append(int(self.table.item(0, c).text()))
            self.OS.append(int(self.table.item(1, c).text()))
            self.Abdomen_simple.append(int(self.table.item(2, c).text()))
            self.UIV.append(int(self.table.item(3, c).text()))
            self.Cholecystographie.append(int(self.table.item(4, c).text()))
            self.Estomac.append(int(self.table.item(5, c).text()))
            self.Echographie.append(int(self.table.item(6, c).text()))
            self.Fibroscopie.append(int(self.table.item(7, c).text()))
            self.ECG.append(int(self.table.item(8, c).text()))

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_homme where state_homme.m =? and state_homme.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_h = cur.fetchall()

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_famme where state_famme.m =? and state_famme.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_f = cur.fetchall()

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_enfant where state_enfant.m =? and state_enfant.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_e = cur.fetchall()

        if res_h:
            sql_q = 'UPDATE state_homme set Poumon =?,OS=?,Abdomen_simple=?,UIV=?,Cholecystographie=?,Estomac=?,Echographie=?,Fibroscopie=?,ECG=? where state_homme.m=? and state_homme.y=?'
            cur.execute(sql_q, (
                self.Poumon[0], self.OS[0], self.Abdomen_simple[0], self.UIV[0], self.Cholecystographie[0],
                self.Estomac[0],
                self.Echographie[0], self.Fibroscopie[0], self.ECG[0], self.month, self.year))
            connection.commit()
        else:
            sql_q = 'INSERT INTO state_homme (m,y,Poumon,OS,Abdomen_simple,UIV,Cholecystographie,Estomac,Echographie,Fibroscopie,ECG) values (?,?,?,?,?,?,?,?,?,?,?)'
            cur.execute(sql_q, (self.month, self.year, self.Poumon[0], self.OS[0], self.Abdomen_simple[0], self.UIV[0],
                                self.Cholecystographie[0], self.Estomac[0], self.Echographie[0], self.Fibroscopie[0],
                                self.ECG[0]))
            connection.commit()

        if res_f:
            sql_q = 'UPDATE state_famme set Poumon =?,OS=?,Abdomen_simple=?,UIV=?,Cholecystographie=?,Estomac=?,Echographie=?,Fibroscopie=?,ECG=? where state_famme.m=? and state_famme.y=?'
            cur.execute(sql_q, (
                self.Poumon[1], self.OS[1], self.Abdomen_simple[1], self.UIV[1], self.Cholecystographie[1],
                self.Estomac[1],
                self.Echographie[1], self.Fibroscopie[1], self.ECG[1], self.month, self.year))
            connection.commit()
        else:
            sql_q = 'INSERT INTO state_famme (m,y,Poumon,OS,Abdomen_simple,UIV,Cholecystographie,Estomac,Echographie,Fibroscopie,ECG) values (?,?,?,?,?,?,?,?,?,?,?)'
            cur.execute(sql_q, (self.month, self.year, self.Poumon[1], self.OS[1], self.Abdomen_simple[1], self.UIV[1],
                                self.Cholecystographie[1], self.Estomac[1], self.Echographie[1], self.Fibroscopie[1],
                                self.ECG[1]))
            connection.commit()

        if res_e:
            sql_q = 'UPDATE state_enfant set Poumon =?,OS=?,Abdomen_simple=?,UIV=?,Cholecystographie=?,Estomac=?,Echographie=?,Fibroscopie=?,ECG=? where state_enfant.m=? and state_enfant.y=?'
            cur.execute(sql_q, (
                self.Poumon[2], self.OS[2], self.Abdomen_simple[2], self.UIV[2], self.Cholecystographie[2],
                self.Estomac[2],
                self.Echographie[2], self.Fibroscopie[2], self.ECG[2], self.month, self.year))
            connection.commit()
        else:
            sql_q = 'INSERT INTO state_enfant (m,y,Poumon,OS,Abdomen_simple,UIV,Cholecystographie,Estomac,Echographie,Fibroscopie,ECG) values (?,?,?,?,?,?,?,?,?,?,?)'
            cur.execute(sql_q, (self.month, self.year, self.Poumon[2], self.OS[2], self.Abdomen_simple[2], self.UIV[2],
                                self.Cholecystographie[2], self.Estomac[2], self.Echographie[2], self.Fibroscopie[2],
                                self.ECG[2]))
            connection.commit()

        for prog in range(20):
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal.emit(True)


class ThreadStateExport(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(list)

    def __init__(self, month, year):
        super(ThreadStateExport, self).__init__()
        self.month = month
        self.year = year
        self.data = [("Examen", "Homme", "Famme", "Enfant", "Total")]

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_homme where state_homme.m =? and state_homme.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_h = cur.fetchall()

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_famme where state_famme.m =? and state_famme.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_f = cur.fetchall()

        sql_q = 'SELECT Poumon, OS, Abdomen_simple, UIV, Cholecystographie, Estomac, Echographie, Fibroscopie, ECG FROM state_enfant where state_enfant.m =? and state_enfant.y =?'
        cur.execute(sql_q, (self.month, self.year))
        res_e = cur.fetchall()

        self.Poumon = []
        self.OS = []
        self.Abdomen_simple = []
        self.UIV = []
        self.Cholecystographie = []
        self.Estomac = []
        self.Echographie = []
        self.Fibroscopie = []
        self.ECG = []

        if res_h:
            res_h = res_h[0]
            po = res_h[0]
            self.Poumon.append(po)
            os = res_h[1]
            self.OS.append(os)
            abd = res_h[2]
            self.Abdomen_simple.append(abd)
            uiv = res_h[3]
            self.UIV.append(uiv)
            chol = res_h[4]
            self.Cholecystographie.append(chol)
            est = res_h[5]
            self.Estomac.append(est)
            echo = res_h[6]
            self.Echographie.append(echo)
            fibr = res_h[7]
            self.Fibroscopie.append(fibr)
            ecg = res_h[8]
            self.ECG.append(ecg)
        else:
            self.Poumon.append(0)
            self.OS.append(0)
            self.Abdomen_simple.append(0)
            self.UIV.append(0)
            self.Cholecystographie.append(0)
            self.Estomac.append(0)
            self.Echographie.append(0)
            self.Fibroscopie.append(0)
            self.ECG.append(0)

        if res_f:
            res_f = res_f[0]
            po = res_f[0]
            self.Poumon.append(po)
            os = res_f[1]
            self.OS.append(os)
            abd = res_f[2]
            self.Abdomen_simple.append(abd)
            uiv = res_f[3]
            self.UIV.append(uiv)
            chol = res_f[4]
            self.Cholecystographie.append(chol)
            est = res_f[5]
            self.Estomac.append(est)
            echo = res_f[6]
            self.Echographie.append(echo)
            fibr = res_f[7]
            self.Fibroscopie.append(fibr)
            ecg = res_f[8]
            self.ECG.append(ecg)
        else:
            self.Poumon.append(0)
            self.OS.append(0)
            self.Abdomen_simple.append(0)
            self.UIV.append(0)
            self.Cholecystographie.append(0)
            self.Estomac.append(0)
            self.Echographie.append(0)
            self.Fibroscopie.append(0)
            self.ECG.append(0)

        if res_e:
            res_e = res_e[0]
            po = res_e[0]
            self.Poumon.append(po)
            os = res_e[1]
            self.OS.append(os)
            abd = res_e[2]
            self.Abdomen_simple.append(abd)
            uiv = res_e[3]
            self.UIV.append(uiv)
            chol = res_e[4]
            self.Cholecystographie.append(chol)
            est = res_e[5]
            self.Estomac.append(est)
            echo = res_e[6]
            self.Echographie.append(echo)
            fibr = res_e[7]
            self.Fibroscopie.append(fibr)
            ecg = res_e[8]
            self.ECG.append(ecg)
        else:
            self.Poumon.append(0)
            self.OS.append(0)
            self.Abdomen_simple.append(0)
            self.UIV.append(0)
            self.Cholecystographie.append(0)
            self.Estomac.append(0)
            self.Echographie.append(0)
            self.Fibroscopie.append(0)
            self.ECG.append(0)

        prog = 0
        total = self.Poumon[0] + self.Poumon[1] + self.Poumon[2]
        data_examen = ("Poumon", self.Poumon[0], self.Poumon[1], self.Poumon[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total = self.OS[0] + self.OS[1] + self.OS[2]
        data_examen = ("OS", self.OS[0], self.OS[1], self.OS[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total = self.Abdomen_simple[0] + self.Abdomen_simple[1] + self.Abdomen_simple[2]
        data_examen = ("Abdomen simple", self.Abdomen_simple[0], self.Abdomen_simple[1], self.Abdomen_simple[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total = self.UIV[0] + self.UIV[1] + self.UIV[2]
        data_examen = ("U.I.V", self.UIV[0], self.UIV[1], self.UIV[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total = self.Cholecystographie[0] + self.Cholecystographie[1] + self.Cholecystographie[2]
        data_examen = (
            "Cholecystographie", self.Cholecystographie[0], self.Cholecystographie[1], self.Cholecystographie[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total = self.Estomac[0] + self.Estomac[1] + self.Estomac[2]
        data_examen = ("Estomac", self.Estomac[0], self.Estomac[1], self.Estomac[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total = self.Echographie[0] + self.Echographie[1] + self.Echographie[2]
        data_examen = ("Echographie", self.Echographie[0], self.Echographie[1], self.Echographie[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total = self.Fibroscopie[0] + self.Fibroscopie[1] + self.Fibroscopie[2]
        data_examen = ("Fibroscopie", self.Fibroscopie[0], self.Fibroscopie[1], self.Fibroscopie[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total = self.ECG[0] + self.ECG[1] + self.ECG[2]
        data_examen = ("E.C.G", self.ECG[0], self.ECG[1], self.ECG[2], total)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))
        prog = prog + 1

        total1 = self.Poumon[0] + self.OS[0] + self.Abdomen_simple[0] + self.UIV[0] + self.Cholecystographie[0] + \
                 self.Estomac[0] + self.Echographie[0] + self.Fibroscopie[0] + self.ECG[0]
        total2 = self.Poumon[1] + self.OS[1] + self.Abdomen_simple[1] + self.UIV[1] + self.Cholecystographie[1] + \
                 self.Estomac[1] + self.Echographie[1] + self.Fibroscopie[1] + self.ECG[1]
        total3 = self.Poumon[2] + self.OS[2] + self.Abdomen_simple[2] + self.UIV[2] + self.Cholecystographie[2] + \
                 self.Estomac[2] + self.Echographie[2] + self.Fibroscopie[2] + self.ECG[2]
        total4 = total1 + total2 + total3

        data_examen = ("Total", total1, total2, total3, total4)
        self.data.append(data_examen)
        time.sleep(0.2)
        self._signal.emit(int(prog))

        connection.close()
        self._signal_result.emit(self.data)


class ThreadAddGroupe(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, name, groupe):
        super(ThreadAddGroupe, self).__init__()
        self.name = name
        self.groupe = groupe

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
        cur.execute(sql_q, (self.name, "urgence_inf"))

        connection.commit()

        id_inf = get_workerId_by_name(self.name, "urgence_inf")
        id_inf = id_inf[0]

        sql_q = "INSERT INTO groupe (g,inf_id) values (?,?)"
        cur.execute(sql_q, (self.groupe, id_inf[0]))

        connection.commit()
        connection.close()

        for n in range(20):
            self._signal.emit(n)
            time.sleep(0.1)

        self._signal_result.emit(True)


class ThreadUpdateGroupe(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, id, name, groupe):
        super(ThreadUpdateGroupe, self).__init__()
        self.name = name
        self.groupe = groupe
        self.id = id

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):

        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        if self.name == "":
            sql_q = 'UPDATE groupe SET g= ? WHERE inf_id= ?'
            cur.execute(sql_q, (self.groupe, self.id))
        elif self.groupe == "":
            sql_q = 'UPDATE health_worker SET full_name= ? WHERE worker_id= ?'
            cur.execute(sql_q, (self.name, self.id))
        else:
            sql_q = 'UPDATE groupe SET g= ? WHERE inf_id= ?'
            cur.execute(sql_q, (self.groupe, self.id))

            sql_q = 'UPDATE health_worker SET full_name= ? WHERE worker_id= ?'
            cur.execute(sql_q, (self.name, self.id))

        connection.commit()
        connection.close()

        for n in range(20):
            self._signal.emit(n)
            time.sleep(0.1)

        self._signal_result.emit(True)


class ThreadGuardUrgenceInf(QThread):
    _signal = pyqtSignal(int)
    _signal_groupes = pyqtSignal(list)
    _signal_result = pyqtSignal(list)
    _signal_finish = pyqtSignal(bool)

    def __init__(self, num_days, month, year):
        super(ThreadGuardUrgenceInf, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year
        self.data = [("Jours", "Date", "De 08h:00 à 16h:00", "De 16h:00 à 08h:00")]

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

            sql_q = 'SELECT guard_groupe.g FROM guard_groupe WHERE guard_groupe.periode =? and guard_groupe.d =? and guard_groupe.m =? and guard_groupe.y =?'
            cur.execute(sql_q, ('light', day, self.month, self.year))
            results_light = cur.fetchall()

            sql_q = 'SELECT guard_groupe.g FROM guard_groupe WHERE guard_groupe.periode =? and guard_groupe.d =? and guard_groupe.m =? and guard_groupe.y =?'
            cur.execute(sql_q, ('night', day, self.month, self.year))
            results_night = cur.fetchall()

            light = ""
            night = ""

            if results_light:
                rl = results_light[0]
                light = light + str(rl[0])

            if results_night:
                rn = results_night[0]
                night = night + str(rn[0])

            data_day = (m, date_day, light, night)

            self.data.append(data_day)

            time.sleep(0.3)
            self._signal.emit(int(prog))

        print(self.data)
        self._signal_result.emit(self.data)

        sql_q = 'SELECT DISTINCT g FROM groupe'
        cur.execute(sql_q)
        groupes = cur.fetchall()

        grs = []

        for groupe in groupes:
            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
            cur.execute(sql_q, (groupe[0],))
            workers = cur.fetchall()
            gr = "Groupe " + groupe[0] + ": "

            for worker in workers:
                gr = gr + worker[0] + " / "

            grs.append(gr)

        self._signal_groupes.emit(grs)
        connection.close()

        self._signal_finish.emit(True)


class Thread_create_urgence_inf_guard(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(bool)

    def __init__(self, num_days, month, year, table):
        super(Thread_create_urgence_inf_guard, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year
        self.table = table

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        for row in range(self.num_days):
            day = row + 1
            prog = row * 100 / self.num_days

            sql_q = 'SELECT guard_groupe.g FROM guard_groupe WHERE guard_groupe.periode =? and guard_groupe.d =? and guard_groupe.m =? and guard_groupe.y =?'
            cur.execute(sql_q, ('light', day, self.month, self.year))
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
                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
                    cur.execute(sql_q, (str(rl[0]),))
                    res1 = cur.fetchall()

                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
                    cur.execute(sql_q, (med_name,))
                    res2 = cur.fetchall()

                    sql_q = 'DELETE FROM guard_groupe WHERE  guard_groupe.d=? and guard_groupe.m=? and guard_groupe.y=? and guard_groupe.periode =? and guard_groupe.g =?'
                    cur.execute(sql_q, (day, self.month, self.year, 'light', str(rl[0])))

                    connection.commit()

                    sql_q = 'INSERT INTO guard_groupe (d,m,y,periode,g) values (?,?,?,?,?)'
                    cur.execute(sql_q, (day, self.month, self.year, 'light', med_name))

                    connection.commit()

                    for id in res1:
                        id = id[0]
                        sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'light', id))

                    for id in res2:
                        id = id[0]
                        sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'light', id))

                elif str(rl[0]) != med_name and med_name == "":

                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
                    cur.execute(sql_q, (str(rl[0]),))
                    res1 = cur.fetchall()

                    sql_q = 'DELETE FROM guard_groupe WHERE  guard_groupe.d=? and guard_groupe.m=? and guard_groupe.y=? and guard_groupe.periode =? and guard_groupe.g =?'
                    cur.execute(sql_q, (day, self.month, self.year, 'light', str(rl[0])))

                    connection.commit()

                    for id in res1:
                        id = id[0]
                        sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'light', id))

            elif med_name != "":

                sql_q = 'INSERT INTO guard_groupe (d,m,y,periode,g) values (?,?,?,?,?)'
                cur.execute(sql_q, (day, self.month, self.year, 'light', med_name))

                connection.commit()

                sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
                cur.execute(sql_q, (med_name,))
                res2 = cur.fetchall()
                for id in res2:
                    id = id[0]
                    sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'light', id))

            # guard shift night :

            sql_q = 'SELECT guard_groupe.g FROM guard_groupe WHERE guard_groupe.periode =? and guard_groupe.d =? and guard_groupe.m =? and guard_groupe.y =?'
            cur.execute(sql_q, ('night', day, self.month, self.year))
            results_night = cur.fetchall()

            if results_night:
                rn = results_night[0]

                if str(rn[0]) == med_name_2:
                    print("do nothing")
                elif str(rn[0]) != med_name_2 and med_name_2 != "":

                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
                    cur.execute(sql_q, (str(rn[0]),))
                    res1 = cur.fetchall()

                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
                    cur.execute(sql_q, (med_name_2,))
                    res2 = cur.fetchall()

                    sql_q = 'DELETE FROM guard_groupe WHERE  guard_groupe.d=? and guard_groupe.m=? and guard_groupe.y=? and guard_groupe.periode =? and guard_groupe.g =?'
                    cur.execute(sql_q, (day, self.month, self.year, 'night', str(rn[0])))

                    connection.commit()

                    sql_q = 'INSERT INTO guard_groupe (d,m,y,periode,g) values (?,?,?,?,?)'
                    cur.execute(sql_q, (day, self.month, self.year, 'night', med_name_2))

                    connection.commit()

                    for id in res1:
                        id = id[0]
                        sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'night', id))

                    for id in res2:
                        id = id[0]
                        sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'night', id))

                elif str(rn[0]) != med_name_2 and med_name_2 == "":
                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
                    cur.execute(sql_q, (str(rn[0]),))
                    res1 = cur.fetchall()

                    sql_q = 'DELETE FROM guard_groupe WHERE  guard_groupe.d=? and guard_groupe.m=? and guard_groupe.y=? and guard_groupe.periode =? and guard_groupe.g =?'
                    cur.execute(sql_q, (day, self.month, self.year, 'night', str(rn[0])))

                    connection.commit()

                    for id in res1:
                        id = id[0]
                        sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'night', id))



            elif med_name_2 != "":

                sql_q = 'INSERT INTO guard_groupe (d,m,y,periode,g) values (?,?,?,?,?)'
                cur.execute(sql_q, (day, self.month, self.year, 'night', med_name_2))

                connection.commit()

                sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id WHERE groupe.g =?'
                cur.execute(sql_q, (med_name_2,))
                res2 = cur.fetchall()

                for id in res2:
                    id = id[0]
                    sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'night', id))

            connection.commit()
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal.emit(True)


class Thread_load_guards_inf_urgences(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(list)
    _signal_finish = pyqtSignal(bool)

    def __init__(self, num_days, month, year):
        super(Thread_load_guards_inf_urgences, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        for row in range(self.num_days):
            day = row + 1
            prog = row * 100 / self.num_days

            sql_q = 'SELECT guard_groupe.g FROM guard_groupe WHERE guard_groupe.periode =? and guard_groupe.d =? and guard_groupe.m =? and guard_groupe.y =?'
            cur.execute(sql_q, ('light', day, self.month, self.year))
            results_light = cur.fetchall()

            sql_q = 'SELECT guard_groupe.g FROM guard_groupe WHERE guard_groupe.periode =? and guard_groupe.d =? and guard_groupe.m =? and guard_groupe.y =?'
            cur.execute(sql_q, ('night', day, self.month, self.year))
            results_night = cur.fetchall()

            list = []
            list.append(row)
            list.append(results_light)
            list.append(results_night)

            self._signal.emit(list)
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal_finish.emit(True)


class ThreadAddGroupeSurv(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, name, groupe):
        super(ThreadAddGroupeSurv, self).__init__()
        self.name = name
        self.groupe = groupe

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
        cur.execute(sql_q, (self.name, "urgence_surv"))

        connection.commit()

        id_inf = get_workerId_by_name(self.name, "urgence_surv")
        id_inf = id_inf[0]

        sql_q = "INSERT INTO groupe_surv (g,inf_id) values (?,?)"
        cur.execute(sql_q, (self.groupe, id_inf[0]))

        connection.commit()
        connection.close()

        for n in range(20):
            self._signal.emit(n)
            time.sleep(0.1)

        self._signal_result.emit(True)


class ThreadUpdateGroupeSurv(QThread):
    _signal = pyqtSignal(int)
    _signal_result = pyqtSignal(bool)

    def __init__(self, id, name, groupe):
        super(ThreadUpdateGroupeSurv, self).__init__()
        self.name = name
        self.groupe = groupe
        self.id = id

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):

        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        if self.name == "":
            sql_q = 'UPDATE groupe_surv SET g= ? WHERE inf_id= ?'
            cur.execute(sql_q, (self.groupe, self.id))
        elif self.groupe == "":
            sql_q = 'UPDATE health_worker SET full_name= ? WHERE worker_id= ?'
            cur.execute(sql_q, (self.name, self.id))
        else:
            sql_q = 'UPDATE groupe_surv SET g= ? WHERE inf_id= ?'
            cur.execute(sql_q, (self.groupe, self.id))

            sql_q = 'UPDATE health_worker SET full_name= ? WHERE worker_id= ?'
            cur.execute(sql_q, (self.name, self.id))

        connection.commit()
        connection.close()

        for n in range(20):
            self._signal.emit(n)
            time.sleep(0.1)

        self._signal_result.emit(True)


class ThreadGuardUrgenceSurv(QThread):
    _signal = pyqtSignal(int)
    _signal_groupes = pyqtSignal(list)
    _signal_result = pyqtSignal(list)
    _signal_finish = pyqtSignal(bool)

    def __init__(self, num_days, month, year):
        super(ThreadGuardUrgenceSurv, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year
        self.data = [("Jours", "Date", "De 08h:00 à 16h:00", "De 16h:00 à 08h:00")]

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

            sql_q = 'SELECT guard_groupe_surv.g FROM guard_groupe_surv WHERE guard_groupe_surv.periode =? and guard_groupe_surv.d =? and guard_groupe_surv.m =? and guard_groupe_surv.y =?'
            cur.execute(sql_q, ('light', day, self.month, self.year))
            results_light = cur.fetchall()

            sql_q = 'SELECT guard_groupe_surv.g FROM guard_groupe_surv WHERE guard_groupe_surv.periode =? and guard_groupe_surv.d =? and guard_groupe_surv.m =? and guard_groupe_surv.y =?'
            cur.execute(sql_q, ('night', day, self.month, self.year))
            results_night = cur.fetchall()

            light = ""
            night = ""

            if results_light:
                rl = results_light[0]
                light = light + str(rl[0])

            if results_night:
                rn = results_night[0]
                night = night + str(rn[0])

            data_day = (m, date_day, light, night)

            self.data.append(data_day)

            time.sleep(0.3)
            self._signal.emit(int(prog))

        print(self.data)
        self._signal_result.emit(self.data)

        sql_q = 'SELECT DISTINCT g FROM groupe_surv'
        cur.execute(sql_q)
        groupes = cur.fetchall()

        grs = []

        for groupe in groupes:
            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
            cur.execute(sql_q, (groupe[0],))
            workers = cur.fetchall()
            gr = "Groupe " + groupe[0] + ": "

            for worker in workers:
                gr = gr + worker[0] + " / "

            grs.append(gr)

        self._signal_groupes.emit(grs)
        connection.close()

        self._signal_finish.emit(True)


class Thread_create_urgence_surv_guard(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(bool)

    def __init__(self, num_days, month, year, table):
        super(Thread_create_urgence_surv_guard, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year
        self.table = table

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        for row in range(self.num_days):
            day = row + 1
            prog = row * 100 / self.num_days

            sql_q = 'SELECT guard_groupe_surv.g FROM guard_groupe_surv WHERE guard_groupe_surv.periode =? and guard_groupe_surv.d =? and guard_groupe_surv.m =? and guard_groupe_surv.y =?'
            cur.execute(sql_q, ('light', day, self.month, self.year))
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
                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
                    cur.execute(sql_q, (str(rl[0]),))
                    res1 = cur.fetchall()

                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
                    cur.execute(sql_q, (med_name,))
                    res2 = cur.fetchall()

                    sql_q = 'DELETE FROM guard_groupe_surv WHERE  guard_groupe_surv.d=? and guard_groupe_surv.m=? and guard_groupe_surv.y=? and guard_groupe_surv.periode =? and guard_groupe_surv.g =?'
                    cur.execute(sql_q, (day, self.month, self.year, 'light', str(rl[0])))

                    connection.commit()

                    sql_q = 'INSERT INTO guard_groupe_surv (d,m,y,periode,g) values (?,?,?,?,?)'
                    cur.execute(sql_q, (day, self.month, self.year, 'light', med_name))

                    connection.commit()

                    for id in res1:
                        id = id[0]
                        sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'light', id))

                    for id in res2:
                        id = id[0]
                        sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'light', id))

                elif str(rl[0]) != med_name and med_name == "":

                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
                    cur.execute(sql_q, (str(rl[0]),))
                    res1 = cur.fetchall()

                    sql_q = 'DELETE FROM guard_groupe_surv WHERE  guard_groupe_surv.d=? and guard_groupe_surv.m=? and guard_groupe_surv.y=? and guard_groupe_surv.periode =? and guard_groupe_surv.g =?'
                    cur.execute(sql_q, (day, self.month, self.year, 'light', str(rl[0])))

                    connection.commit()

                    for id in res1:
                        id = id[0]
                        sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'light', id))

            elif med_name != "":

                sql_q = 'INSERT INTO guard_groupe_surv (d,m,y,periode,g) values (?,?,?,?,?)'
                cur.execute(sql_q, (day, self.month, self.year, 'light', med_name))

                connection.commit()

                sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
                cur.execute(sql_q, (med_name,))
                res2 = cur.fetchall()
                for id in res2:
                    id = id[0]
                    sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'light', id))

            # guard shift night :

            sql_q = 'SELECT guard_groupe_surv.g FROM guard_groupe_surv WHERE guard_groupe_surv.periode =? and guard_groupe_surv.d =? and guard_groupe_surv.m =? and guard_groupe_surv.y =?'
            cur.execute(sql_q, ('night', day, self.month, self.year))
            results_night = cur.fetchall()

            if results_night:
                rn = results_night[0]

                if str(rn[0]) == med_name_2:
                    print("do nothing")
                elif str(rn[0]) != med_name_2 and med_name_2 != "":

                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
                    cur.execute(sql_q, (str(rn[0]),))
                    res1 = cur.fetchall()

                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
                    cur.execute(sql_q, (med_name_2,))
                    res2 = cur.fetchall()

                    sql_q = 'DELETE FROM guard_groupe_surv WHERE  guard_groupe_surv.d=? and guard_groupe_surv.m=? and guard_groupe_surv.y=? and guard_groupe_surv.periode =? and guard_groupe_surv.g =?'
                    cur.execute(sql_q, (day, self.month, self.year, 'night', str(rn[0])))

                    connection.commit()

                    sql_q = 'INSERT INTO guard_groupe_surv (d,m,y,periode,g) values (?,?,?,?,?)'
                    cur.execute(sql_q, (day, self.month, self.year, 'night', med_name_2))

                    connection.commit()

                    for id in res1:
                        id = id[0]
                        sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'night', id))

                    for id in res2:
                        id = id[0]
                        sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'night', id))

                elif str(rn[0]) != med_name_2 and med_name_2 == "":
                    sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
                    cur.execute(sql_q, (str(rn[0]),))
                    res1 = cur.fetchall()

                    sql_q = 'DELETE FROM guard_groupe_surv WHERE  guard_groupe_surv.d=? and guard_groupe_surv.m=? and guard_groupe_surv.y=? and guard_groupe_surv.periode =? and guard_groupe_surv.g =?'
                    cur.execute(sql_q, (day, self.month, self.year, 'night', str(rn[0])))

                    connection.commit()

                    for id in res1:
                        id = id[0]
                        sql_q_light = 'DELETE FROM guard WHERE guard.d=? and guard.m=? and guard.y=? and guard.periode =? and guard.gardien_id =?'
                        cur.execute(sql_q_light, (day, self.month, self.year, 'night', id))



            elif med_name_2 != "":

                sql_q = 'INSERT INTO guard_groupe_surv (d,m,y,periode,g) values (?,?,?,?,?)'
                cur.execute(sql_q, (day, self.month, self.year, 'night', med_name_2))

                connection.commit()

                sql_q = 'SELECT health_worker.worker_id FROM health_worker INNER JOIN groupe_surv ON health_worker.worker_id = groupe_surv.inf_id WHERE groupe_surv.g =?'
                cur.execute(sql_q, (med_name_2,))
                res2 = cur.fetchall()

                for id in res2:
                    id = id[0]
                    sql_q_light = 'INSERT INTO guard (d,m,y,periode,gardien_id) values (?,?,?,?,?)'
                    cur.execute(sql_q_light, (day, self.month, self.year, 'night', id))

            connection.commit()
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal.emit(True)


class Thread_load_guards_surv_urgences(QThread):
    _signal_status = pyqtSignal(int)
    _signal = pyqtSignal(list)
    _signal_finish = pyqtSignal(bool)

    def __init__(self, num_days, month, year):
        super(Thread_load_guards_surv_urgences, self).__init__()
        self.num_days = num_days
        self.month = month
        self.year = year

    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()

        for row in range(self.num_days):
            day = row + 1
            prog = row * 100 / self.num_days

            sql_q = 'SELECT guard_groupe_surv.g FROM guard_groupe_surv WHERE guard_groupe_surv.periode =? and guard_groupe_surv.d =? and guard_groupe_surv.m =? and guard_groupe_surv.y =?'
            cur.execute(sql_q, ('light', day, self.month, self.year))
            results_light = cur.fetchall()

            sql_q = 'SELECT guard_groupe_surv.g FROM guard_groupe_surv WHERE guard_groupe_surv.periode =? and guard_groupe_surv.d =? and guard_groupe_surv.m =? and guard_groupe_surv.y =?'
            cur.execute(sql_q, ('night', day, self.month, self.year))
            results_night = cur.fetchall()

            list = []
            list.append(row)
            list.append(results_light)
            list.append(results_night)

            self._signal.emit(list)
            time.sleep(0.1)
            self._signal_status.emit(int(prog))

        connection.close()
        self._signal_finish.emit(True)


class ThreadLoadInf(QThread):
    _signal_status = pyqtSignal(int)
    _signal_inf = pyqtSignal(list)
    _signal_surv = pyqtSignal(list)
    _signal_finish = pyqtSignal(bool)

    def __init__(self):
        super(ThreadLoadInf, self).__init__()
    def __del__(self):
        self.terminate()
        self.wait()

    def run(self):

        infirmiers = load_groupes_inf()
        surveillants = load_groupes_surv()

        for i in range(30):
            self._signal_status.emit(i)

        list_inf = []
        ind_inf = 0
        for inf in infirmiers:
            list_inf.append(ind_inf)
            list_inf.append(inf)
            self._signal_inf.emit(list_inf)
            ind_inf = ind_inf + 1

        list_surv = []
        ind_surv = 0
        for surv in surveillants:
            list_surv.append(ind_surv)
            list_surv.append(surv)
            self._signal_surv.emit(list_surv)
            ind_surv = ind_surv + 1

        for i in range(31, 99):
            self._signal_status.emit(i)

        self._signal_finish.emit(True)






