import datetime

now = datetime.datetime.now()
print(now.isoformat())
import time
time.sleep(2)
print(datetime.datetime.now() - now)