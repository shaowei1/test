from bili import BiliBili
from progress import ShowProcess
import sys, time

if __name__ == '__main__':
    max_steps = 100
    process_bar = ShowProcess(max_steps, 'OK')

    print(sys.argv)
    url = sys.argv[2]

    for i in range(max_steps):
        process_bar.show_process()
        time.sleep(0.1)
