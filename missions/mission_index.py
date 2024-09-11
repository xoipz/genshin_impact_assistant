"""This file is generated automatically. Do not manually modify it."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MISSION_INDEX = ['MissionAutoCollector', 'MissionQingXin2', 'MissionSakuraBloom1', 'MissionSweatFlower2', 'MissionVioletgrass2']
def get_mission_object(mission_name:str):
    if mission_name == 'MissionAutoCollector':
        import source.mission.missions.MissionAutoCollector
        return source.mission.missions.MissionAutoCollector.MissionMain()
    if mission_name == 'MissionQingXin2':
        import source.mission.missions.MissionQingXin2
        return source.mission.missions.MissionQingXin2.MissionMain()
    if mission_name == 'MissionSakuraBloom1':
        import source.mission.missions.MissionSakuraBloom1
        return source.mission.missions.MissionSakuraBloom1.MissionMain()
    if mission_name == 'MissionSweatFlower2':
        import source.mission.missions.MissionSweatFlower2
        return source.mission.missions.MissionSweatFlower2.MissionMain()
    if mission_name == 'MissionVioletgrass2':
        import source.mission.missions.MissionVioletgrass2
        return source.mission.missions.MissionVioletgrass2.MissionMain()
