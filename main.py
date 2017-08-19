from pyqqclient.SmartqqClient import SmartqqClient
from threading import Thread
import time

if __name__ == '__main__':
    client = SmartqqClient()
    client_thread = Thread(target=client.run)
    client_thread.start()
