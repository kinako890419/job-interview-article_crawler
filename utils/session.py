from requests.adapters import HTTPAdapter
import requests
from urllib3.util.retry import Retry
import time
import random


def create_session_with_retry():
    """
    創建具有重試機制的session
    """
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def random_sleep():
    """
    隨機延遲N秒
    """
    sleep_time = random.uniform(1, 3)
    print(f"等待 {sleep_time:.2f} 秒...")
    time.sleep(sleep_time)
