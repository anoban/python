import time
for i in range(100):
    print(f"Iteration: {i:4d}", end = '')
    time.sleep(0.1)
    print("\r\r\r\r", end = '')     # deleting the last four printed characters will be enough
print("")    
