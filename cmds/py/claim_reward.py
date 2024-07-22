import os
import sys

current_file_path = __file__
directory_path = os.path.dirname(current_file_path)
root_path = os.path.join(directory_path, "..", "..")
sys.path.append(root_path)

from utils.windowUtils import focus_on_program
from source.task.claim_reward.claim_reward import ClaimRewardMission, ClaimRewardTask

if __name__ == '__main__':
    focus_on_program("原神")
    crm = ClaimRewardMission()
    r = crm._exec_dispatch()
    crt = ClaimRewardTask()
    crt.start()
