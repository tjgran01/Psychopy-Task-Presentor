import time

count = 0
while(True):
    if input("t"):
        count += 1
        time = time.time()
        write_output(count, time)
