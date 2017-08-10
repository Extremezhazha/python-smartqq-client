from SmartQQLoginPipeline import SmartQQLoginPipeline
import requests
import shutil

if __name__ == '__main__':
    accumulated, response = SmartQQLoginPipeline(requests.Session()).run()
    print(accumulated)
