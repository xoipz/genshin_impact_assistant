import sys
import os
current_file_path = __file__
directory_path = os.path.dirname(current_file_path)
root_path = os.path.join(directory_path,"..","..")
sys.path.append(root_path)
from utils.windowUtils import focus_on_program



from source.commission.util import *
from source.task.task_template import TaskTemplate
from source.commission.commission_parser import CommissionParser
from source.commission.commission_acquisition import get_commission_object
from source.ui.ui import ui_control
from source.ui import page as UIPage

class CommissionExecutor(TaskTemplate, CommissionParser):
    def __init__(self):
        super().__init__()
        self.setName("CommissionExecutor")
            
        self._set_and_save_and_load_commission_dicts() # 扫描,加载委托
        self.exec_times = 0
        self.EXEC_LIMIT = 3
        
    def loop(self):
        for i in self.commission_dicts:
            co = get_commission_object(i["type"], i["position"]) # 获得委托对象
            if not co: # commission obj not exist/cannot get obj
                continue
            if i["done"]: # this commission obj has been done.
                logger.info(f"{i['type']} has been done.")
                continue
            ui_control.ensure_page(UIPage.page_main)
            self._add_sub_threading(co)
            co.continue_threading() # start commission obj
            while 1:
                time.sleep(2)
                if self.checkup_stop_func(): return
                if co.pause_threading_flag: break
            self._clean_sub_threading()
            if co.is_commission_succ:
                j = load_json(json_name="commission_dict.json", folder_path=rf"{CONFIG_PATH}\commission")
                j[self.commission_dicts.index(i)]["done"]=True
                save_json(j ,json_name="commission_dict.json", default_path=rf"{CONFIG_PATH}\commission")
        r = self._set_and_save_and_load_commission_dicts()
        if not r:
            logger.info(t2t("Commission(s) Failed, Commission Task end."))
            self.pause_threading()
        if len(self.commission_dicts)==0:
            logger.info(t2t("Cannot find any commissions, Commission Task end."))
            self.stop_threading()
        if self.exec_times >= self.EXEC_LIMIT:
            logger.info(t2t("Number of executions exceeding the limit, Commission Task end."))
            self.pause_threading()
        self.exec_times+=1

# FIXME:Commission
if __name__ == '__main__':
    print('启动')
    focus_on_program("原神")
    ce = CommissionExecutor()
    ce.start()
    ce.continue_threading()
    while not ce.stop_threading_flag:
        time.sleep(1)
    print("Commission Task end")