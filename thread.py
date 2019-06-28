import threading
i = 0

def foo():
    print(i)
    time.sleep(5)

threading.start(foo,())

while True:
    i = i+1