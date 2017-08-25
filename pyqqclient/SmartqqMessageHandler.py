from .MessageHandler import MessageHandler
from .MessageErrcodeException import MessageErrcodeException


class SmartqqMessageHandler(MessageHandler):
    @staticmethod
    def friend_message_filter(message):
        return message["poll_type"] == "message"

    @staticmethod
    def group_message_filter(message):
        return message["poll_type"] == "group_message"

    @staticmethod
    def friend_message_print_handler(message):
        print("this is a friend message")
        return False

    @staticmethod
    def group_message_print_handler(message):
        print("this is a group message")
        return False

    @staticmethod
    def any_message_handler(message):
        print("this message has been ignored")
        return False

    @staticmethod
    def print_all_handler(message_preprocess = None, friend_message_handler=None, group_message_handler=None):

        # def message_preprocess(data):
        #     message = data.json()
        #     if "errcode" in message:
        #         print(message)
        #         raise MessageErrcodeException
        #     if "result" not in message:
        #         print(message)
        #         raise MessageErrcodeException
        #     return message["result"][0]
        result = SmartqqMessageHandler(message_preprocess) if message_preprocess is not None else SmartqqMessageHandler()
        result.add_handler(SmartqqMessageHandler.friend_message_filter,
                           friend_message_handler if friend_message_handler is not None
                           else SmartqqMessageHandler.friend_message_print_handler)
        result.add_handler(SmartqqMessageHandler.group_message_filter,
                           group_message_handler if group_message_handler is not None
                           else SmartqqMessageHandler.group_message_print_handler)
        result.add_handler(SmartqqMessageHandler.any, SmartqqMessageHandler.any_message_handler)
        return result
