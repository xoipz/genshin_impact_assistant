import logger
from source.integration_json.utils import *
from source.integration_json import JIApi
from source.map.extractor.convert import MapConverter

def correction_collection_position(pos:list, name:str='', threshold=15):
    """

    Args:
        pos: Tianli format
        name: the name of collection

    Returns:
        corrected position, Tianli format.

    magic number: offset.

    """
    possible_list = []
    if name != '':
        possible_list = JIApi.data[name]
    else:
        for i in JIApi.data.values():
            for j in i:
                possible_list.append(j)
    possible_pos = []
    for i in possible_list:
        i: PositionJson
        possible_pos.append(MapConverter.convert_GenshinMap_to_cvAutoTrack(i.position))
    logger.debug(f'{len(possible_pos)}')
    offset = threshold
    ed_value_list = quick_euclidean_distance_plist(pos, possible_pos)
    if min(ed_value_list) < offset:
        min_ed = quick_sort_euclidean_distance_plist(pos, possible_pos)[0]
        rp = min_ed
        logger.info(f"position correct succ: {pos} -> {rp}; name:{name}")
        return rp
    else:
        logger.info(f"position correct fail: {pos}; name:{name}")
        return pos


if __name__ == '__main__':
    correction_collection_position([0,0],'海灵芝')