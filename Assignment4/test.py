import time
from datetime import datetime
pt = datetime.strptime(timestring,'%H:%M:%S,%f')
total_seconds = pt.second + pt.minute*60 + pt.hour*360()

while True:
    print(seconds)