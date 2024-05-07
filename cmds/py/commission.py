import os
import sys

current_file_path = __file__
directory_path = os.path.dirname(current_file_path)
root_path = os.path.join(directory_path, "..", "..")
sys.path.append(root_path)

import time

from source.commission.commission_executor import CommissionExecutor
from source.task.claim_reward.claim_reward import ClaimRewardMission, ClaimRewardTask
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

    focus_on_program("原神")
    crm = ClaimRewardMission()
    r = crm._exec_dispatch()
    crt = ClaimRewardTask()
    crt.start()

    print("领取 Task end")
