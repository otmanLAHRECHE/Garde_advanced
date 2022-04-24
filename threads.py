from PyQt5.QtCore import QThread, pyqtSignal

from database_operations import load_workers, add_worker, update_worker, delete_worker, load_garde_month, \
    add_garde_month, check_month


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

        for worker in workers:
            self._signal_list.emit(worker)

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

        for month in months:
            self._signal_list.emit(month)

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

            self._signal_result.emit(True)

