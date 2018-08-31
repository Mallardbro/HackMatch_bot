import time

from directkeys import PressKey, ReleaseKey, J

print("ready...")
time.sleep(3)

PressKey(J)
time.sleep(0.017)
ReleaseKey(J)
time.sleep(0.017)

PressKey(J)
ReleaseKey(J)
