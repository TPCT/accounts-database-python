from concurrent.futures import ThreadPoolExecutor
from requests import get
from threading import Lock

lock = Lock()


def main():
    accounts = get('https://api-accounts.avkngeeks.com/accounts')
    with lock:
        print(accounts.json())


with ThreadPoolExecutor() as e:
    for i in range(5000):
        e.submit(main)