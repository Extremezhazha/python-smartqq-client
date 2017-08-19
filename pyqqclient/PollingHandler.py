import time


class PollingHandler:
    def __init__(self, target, value_handler, delay=None, pass_through_exceptions=None, exception_handler=None):
        self.target = target
        self.value_handler = value_handler
        self.delay = delay
        self.pass_through_exceptions = pass_through_exceptions
        self.exception_handler = exception_handler

    def run(self):
        while True:
            try:
                value = self.target()
                if self.value_handler(value):
                    return value
                if self.delay is not None:
                    time.sleep(self.delay)
            except Exception as ex:
                if (self.pass_through_exceptions is None) or (ex.__class__ in self.pass_through_exceptions):
                    raise ex
                else:
                    if self.exception_handler is not None:
                        if self.exception_handler(ex):
                            return ex
