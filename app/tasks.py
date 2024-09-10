import time

def example(seconds):
    print('Starting Tasks')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print('Tasks Completed')
