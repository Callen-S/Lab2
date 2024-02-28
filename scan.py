import time
import picar_4wd as fc
from heading import update_grid

def good_list(scan_list):
    if not scan_list:
        return False
    if len(scan_list) ==10:
        return True
    else:
        print(len(scan_list))
        return False



def scan(crap, result):
    scan_list = False

    while not good_list(scan_list):
        scan_list = fc.scan_step(35)

    print(scan_list)
    end_time = time.time()
    print(type(scan_list))
    object_stac = []
    if sum(scan_list) < 19:
        if sum(scan_list[:4]) < 7:
            object_stac.append('Left')
        if  sum(scan_list[3:7]) < 7:
             object_stac.append('Infront')
        if  sum(scan_list[3:7]) < 7:
             object_stac.append('Right')
    result.put(object_stac)





