from PyQt5.QtCore import QThread, pyqtSignal

from database_operations import load_workers, add_worker, update_worker, delete_worker


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

    def __init__(self, service, name, op):
        super(ThreadAddWorker, self).__init__()
        self.service = service
        self.name = name
        self.op = op

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
