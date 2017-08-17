class MessageHandler:
    def __init__(self, message_preprocess=lambda x: x):
        self.handler_map = []
        self.message_preprocess = message_preprocess

    def add_handler(self, message_filter: callable, message_handler: callable):
        self.handler_map.append((message_filter, message_handler))

    @staticmethod
    def any(message):
        return True

    def run(self, raw_message):
        message = self.message_preprocess(raw_message)
        for handler_pair in self.handler_map:
            if handler_pair[0](message):
                return handler_pair[1](message)

    def __call__(self, message):
        return self.run(message)
