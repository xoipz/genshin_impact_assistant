from source.map.detection.bigmap import BigMap
from source.map.detection.minimap import MiniMap
from source.map.extractor.convert import MapConverter
from source.util import *
from source.funclib import scene_lib
from source.interaction.interaction_core import itt
from source.map.data.teleporter import DICT_TELEPORTER
from source.manager import asset, posi_manager, scene_manager
from source.common import timer_module
REGION_TEYVAT = [
    "Inazuma",
    "Liyue",
    "Mondstadt",
    "Sumeru"
]
class Map(MiniMap, BigMap, MapConverter):
    
    def __init__(self):
        MiniMap.__init__(self)
        BigMap.__init__(self)
        MapConverter.__init__(self)
        self._upd_smallmap()
        self._upd_bigmap()

    def _upd_smallmap(self):
        if scene_lib.get_current_pagename() == "main":
            self.update_position(itt.capture(jpgmode=0))

    def _upd_bigmap(self):
        if scene_lib.get_current_pagename() == "bigmap":
            self.update_bigmap(itt.capture(jpgmode=0))

    def get_smallmap_posi(self):
        self._upd_smallmap()
        return self.convert_GIMAP_to_cvAutoTrack(self.position)

    def get_bigmap_posi(self, is_upd = True):
        if is_upd:
            self._upd_bigmap()
        logger.info(f"bigmap posi: {self.convert_GIMAP_to_cvAutoTrack(self.bigmap)}")
        return self.convert_GIMAP_to_cvAutoTrack(self.bigmap)

    def _move_bigmap(self, target_posi, float_posi = 0):
        """move bigmap center to target position

        Args:
            target_posi (_type_): 目标坐标
            float_posi (int, optional): 如果点到了什么东东导致移动失败，自动增加该值. Defaults to 0.

        Returns:
            _type_: _description_
        """
        
        """需要处理的异常：

        1. 点击到某个东西弹出右侧弹框
        2. 点击到一坨按键弹出一坨东西
        """
        
        if IS_DEVICE_PC:
            itt.move_to(1920/2+float_posi, 1080/2+float_posi) # screen center
        else:
            itt.move_to(1024/2+float_posi, 768/2+float_posi)
        
        itt.left_down()
        if IS_DEVICE_PC:
            for i in range(5): # 就是要这么多次(
                itt.move_to(10,10,relative=True)
                if i%2==0:
                    itt.left_down()
            for i in range(5):
                itt.move_to(-10,-10,relative=True)
                if i%2==0:
                    itt.left_down()
        curr_posi = self.get_bigmap_posi()
        dx = min( (curr_posi[0] - target_posi[0])*self.MAP_POSI2MOVE_POSI_RATE, self.BIGMAP_MOVE_MAX)
        dx = max( (curr_posi[0] - target_posi[0])*self.MAP_POSI2MOVE_POSI_RATE, -self.BIGMAP_MOVE_MAX)
        dy = min( (curr_posi[1] - target_posi[1])*self.MAP_POSI2MOVE_POSI_RATE, self.BIGMAP_MOVE_MAX)
        dy = max( (curr_posi[1] - target_posi[1])*self.MAP_POSI2MOVE_POSI_RATE, -self.BIGMAP_MOVE_MAX)

        logger.info(f"curr: {curr_posi} target: {target_posi}")
        logger.info(f"_move_bigmap: {dx} {dy}")

        itt.move_to(dx, dy, relative=True)
        itt.delay(0.2, comment="waiting genshin")
        itt.left_up()

        self.get_bigmap_posi()
        if euclidean_distance(self.get_bigmap_posi(is_upd=False), target_posi) <= self.BIGMAP_TP_OFFSET:
            return True
        else:
            itt.delay(0.2, comment="wait for a moment")
            if euclidean_distance(self.get_bigmap_posi(is_upd=False), curr_posi) <= self.BIGMAP_TP_OFFSET:
                self._move_bigmap(target_posi = target_posi, float_posi = float_posi + 45)
            else:
                self._move_bigmap(target_posi = target_posi)
    
    def _find_closest_teleporter(self, posi:list, regions = REGION_TEYVAT):
        """
        return closest teleporter position
        """
        min_dist = 99999
        min_point = [9999,9999]
        min_type = ""
        for i in DICT_TELEPORTER:
            if DICT_TELEPORTER[i].region in regions:
                i_posi = self.convert_GIMAP_to_cvAutoTrack(DICT_TELEPORTER[i].position)
                i_dist = euclidean_distance(posi, i_posi)
                if i_dist < min_dist:
                    min_point = i_posi
                    min_dist = i_dist
                    min_type = DICT_TELEPORTER[i].tp
        return min_point, min_type

    def bigmap_tp(self, posi:list, tp_mode = 0):
        """

        传送到指定坐标。
        模式: 
        0: 自动选择最近的可传送目标传送
        
        移动到地图中心才会传送，因为懒不想算地图与坐标比例(
        
        """
        scene_lib.switch_to_page(scene_manager.page_bigmap, lambda:False)
        if tp_mode == 0:
            # tp_posi = posi
            tp_posi, tp_type = self._find_closest_teleporter(posi)
        self._move_bigmap(tp_posi)
        if tp_type == "Domain":
            logger.debug("tp to Domain")
            # 点一下“仅查看秘境”
        if IS_DEVICE_PC:
            itt.move_and_click([1920/2, 1080/2]) # screen center
        else:
            itt.move_and_click([1024/2, 768/2])
        if tp_type == "Domain":
            logger.debug("tp to Domain")
            # 点回去“仅查看秘境”
        tp_timeout_1 = timer_module.TimeoutTimer(45)
        while 1:            
            if itt.appear_then_click(asset.bigmap_tp) : break
            if tp_type == "Teleporter":
                logger.debug("tp to Teleporter")
                itt.appear_then_click(asset.CSMD)
            elif tp_type == "Statue":
                logger.debug("tp to Statue")
                itt.appear_then_click(asset.QTSX)
            if tp_timeout_1.istimeout():
                scene_lib.switch_to_page(scene_manager.page_bigmap, lambda:False)
                if IS_DEVICE_PC:
                    itt.move_and_click([1920/2, 1080/2]) # screen center
                else:
                    itt.move_and_click([1024/2, 768/2])
                tp_timeout_1.reset()
            time.sleep(0.5)

        # itt.move_and_click([posi_manager.tp_button[0], posi_manager.tp_button[1]], delay=1)
        
        while not (scene_lib.get_current_pagename() == "main"):
            time.sleep(1)
        
if __name__ == '__main__':
    mappp = Map()
    mappp.bigmap_tp([0,-1000])