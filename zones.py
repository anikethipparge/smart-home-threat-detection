# utils/zones.py
import cv2

def is_in_zone(bbox, zone):
    obj_x1, obj_y1, obj_x2, obj_y2 = bbox
    zone_x1, zone_y1, zone_x2, zone_y2 = zone
    return not (obj_x2 < zone_x1 or obj_x1 > zone_x2 or obj_y2 < zone_y1 or obj_y1 > zone_y2)

def draw_zones(frame, zones):
    for zone_name, coords in zones.items():
        x1, y1, x2, y2 = coords
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, zone_name.upper(), (x1, y1-8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2)