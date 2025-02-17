
from source.manager.asset import *
from source.common.timer_module import Timer, AdvanceTimer
from source.ui.page import *
from threading import Lock

from source.interaction.interaction_core import itt
from source.exceptions.ui import *



class UI():
    
    def __init__(self) -> None:
        self.switch_ui_lock = Lock()
    
    ui_pages=[page_bigmap,
              page_domain,
              page_main,
              page_esc,
              page_time,
              page_configure_team]

    def ui_additional(self):
        """
        Handle all annoying popups during UI switching.
        """
        if page_loading.is_current_page(itt):
            while page_loading.is_current_page(itt):
                itt.delay(1, comment='genshin is loading...')

        pass

    def is_valid_page(self):
        if self.get_page(raise_exception=False, max_retry=2) is not None:
            return True
        else:
            return False

    def get_page(self, retry_times=0, raise_exception = True, max_retry=5):
        ret_page = None

        # when ui_addition is complete, enable it
        if raise_exception and False:
            if retry_times >= max_retry:
                raise PageNotFoundError

        for page in self.ui_pages:
            if page.is_current_page(itt, print_log = True):
                if ret_page is None:
                    ret_page = page
                else:
                    logger.warning(f"检测到多个Page")
        if ret_page is None:
            logger.warning(t2t("未知Page, 重新检测"))
            self.ui_additional()
            time.sleep(3)
            ret_page = self.get_page(retry_times=retry_times+1)
        return ret_page

    def verify_page(self, page:UIPage) -> bool:
        return page.is_current_page(itt)

    def ui_goto(self, destination:UIPage, confirm_wait=0.5):
        """
        Args:
            destination (Page):
            confirm_wait:
        """

        retry_timer = AdvanceTimer(1)
        self.switch_ui_lock.acquire()
        # Reset connection
        for page in self.ui_pages:
            page.parent = None


        # Create connection
        visited = [destination]
        visited = set(visited)
        while 1:
            new = visited.copy()
            for page in visited:
                for link in self.ui_pages:
                    if link in visited:
                        continue
                    if page in link.links:
                        link.parent = page
                        new.add(link)
            if len(new) == len(visited):
                break
            visited = new

        print(3)
        logger.info(f"UI goto {destination}")
        confirm_timer = AdvanceTimer(confirm_wait, count=1)
        timeout_timer = AdvanceTimer(5)
        while 1:
            # GOTO_MAIN.clear_offset()
            # if skip_first_screenshot:
            #     skip_first_screenshot = False
            # else:
            #     self.device.screenshot()

            # Destination page
            if destination.is_current_page(itt):
                if confirm_timer.reached():
                    logger.debug(f'Page arrive: {destination}')
                    break
            else:
                confirm_timer.reset()

            # Other pages
            clicked = False
            for page in visited:
                if page.parent is None or len(page.check_icon_list)==0:
                    continue
                if page.is_current_page(itt):
                    logger.debug(f'Page switch: {page} -> {page.parent}')
                    # if retry_timer.reached():
                    button = page.links[page.parent]
                    if isinstance(button,str):
                        if retry_timer.reached():
                            itt.key_press(button)
                            retry_timer.reset()
                    elif isinstance(button,Button):
                        itt.appear_then_click(button)
                    clicked = True
                    confirm_timer.reset()
                        # retry_timer.reset()
                    # else:
                    #     itt.delay(0.2) # wait
                    #     break
                # if self.appear(page.check_button, offset=offset, interval=5):
                #     logger.info(f'Page switch: {page} -> {page.parent}')
                #     button = page.links[page.parent]
                #     self.device.click(button)
                #     self.ui_button_interval_reset(button)
                #     confirm_timer.reset()
                #     clicked = True
                #     break
            if clicked:
                continue

            # Additional
            if self.ui_additional():
                continue

        # Reset connection
        for page in self.ui_pages:
            page.parent = None
        self.switch_ui_lock.release()
        itt.delay(0.5, comment="ui goto is waiting genshin animation")
        # itt.wait_until_stable()
    
    def ensure_page(self, page:UIPage):
        if not self.verify_page(page):
            self.ui_goto(page)
        
ui_control = UI()

if __name__ == '__main__':
    ui = UI()
    # ui.ui_goto(page_main)

    print(ui.ui_pages[0].is_current_page(itt))