from multiprocessing import Process
from .PollingHandler import PollingHandler


class SynchronousPollingHandler:
    def __init__(self, target, value_handler, delay=None, pass_through_exceptions=None, exception_handler=None):
        self.polling_handler = PollingHandler(target, value_handler,
                                              delay=delay,
                                              pass_through_exceptions=pass_through_exceptions,
                                              exception_handler=exception_handler)
        self.polling_process = Process(target=self.polling_handler.run)

    def start(self):
        self.polling_process.start()

    def terminate(self):
        self.polling_process.terminate()
