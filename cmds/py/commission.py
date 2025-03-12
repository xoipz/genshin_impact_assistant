import os
import sys

current_file_path = __file__
directory_path = os.path.dirname(current_file_path)
root_path = os.path.join(directory_path, "..", "..")
sys.path.insert(0, root_path)

import time
from source.commission.commission_executor import CommissionExecutor
from utils.windowUtils import focus_on_program

if __name__ == '__main__':
    print('启动')
    focus_on_program("原神")
    ce = CommissionExecutor()
    ce.start()
    ce.continue_threading()
    while not ce.stop_threading_flag:
        time.sleep(1)
    print("日常 Task end")
