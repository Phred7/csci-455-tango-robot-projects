from typing import Dict


class Controller:

    def __init__(self) -> None:
        servo_robot_anatomy_map: Dict[str: int] = {"motors": 0x01,
                                                   "waist": 0x02,
                                                   "head_pan": 0x03,
                                                   "head_tilt": 0x04,
                                                   "r_shoulder": 0x05,
                                                   "r_bicep": 0x06,
                                                   "r_elbow": 0x07,
                                                   "r_wrist_tilt": 0x08,
                                                   "r_wrist_pan": 0x09,
                                                   "r_grip": 0x10,
                                                   "l_shoulder": 0x12,
                                                   "l_bicep": 0x13,
                                                   "l_elbow": 0x14,
                                                   "l_wrist_tilt": 0x15,
                                                   "l_wrist_pan": 0x16,
                                                   "l_grip": 0x17
                                                   }
        pass

    def

