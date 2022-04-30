import platform
from time import sleep
from typing import Dict, List

import serial
from serial import SerialException


class Controller:

    def __init__(self) -> None:
        self.five_steps_of_POWER: Dict[int:int] = {0: 4000,  # r_high
                                                   1: 5000,  # r_low
                                                   2: 6000,  # mid
                                                   3: 7000,  # l_low
                                                   4: 8000}  # l_high

        self.servo_robot_anatomy_map: Dict[str: int] = {"waist": 0x00,
                                                        "motors": 0x01,
                                                        "turn_motors": 0x02,
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
        self.servo_controller = Controller.servo_controller_via_serial()
        self.servo_min: int = 4000
        self.servo_neutral: int = 6000
        self.servo_max: int = 8000
        self.twist_neutral: int = 2
        self.head_nod_pos: int = 2
        self.head_pan_pos: int = 2
        self.twist_position: int = self.twist_neutral
        self.left_arm_position: int = 0
        self.right_arm_position: int = 0
        self.motor_velocity_counter: int = self.servo_neutral
        self.motor_turn_velocity_counter: int = self.servo_neutral
        self.motor_step_size: int = 64
        if self.servo_controller is None:
            print(f"No servo controller found on {platform.system()} serial port")
            print("Running in servo-less mode.")
        else:
            print(f"Servo controller found on {self.servo_controller.name}")
        # self.drive_servo("turn_motors", self.servo_neutral)

    @staticmethod
    def servo_controller_via_serial():
        """
        Looks for an attached servo driver based on the OS of the runner.
        :return: None or the servo driver as a serial device.
        """
        if platform.system() == 'Linux':
            try:
                device = serial.Serial('/dev/ttyACM0')
                return device
            except SerialException:
                try:
                    device = serial.Serial('/dev/ttyACM1')
                    return device
                except SerialException:
                    return None
        elif platform.system() == 'Windows':
            try:
                device = serial.Serial('COM21')  # COM21
                return device
            except SerialException:
                return None
        elif platform.system() == 'Darwin':
            print("Sorry Connie... mac os is not supported yet. For servos but it is for printing!")
            return None
        else:
            return None

    def drive_servo(self, servo_to_control: str, target: int) -> None:
        """
        Protocol: 0xAA, device number byte, command byte with MSB cleared, any necessary data
        bytes
        :param servo_to_control:
        :param target:
        :return:
        """
        lsb = target & 0x7F
        msb = (target >> 7) & 0x7F
        serial_command = chr(0xaa) + chr(0xC) + chr(0x04) + chr(int(self.servo_robot_anatomy_map.get(servo_to_control))) + chr(
            lsb) + chr(msb)
        self.servo_controller.write(serial_command.encode('utf-8'))
        # print(f"moved {servo} on port 0x{int(self.servo_robot_anatomy_map.get(servo))} to {target}")

    def drive_multiple_servos(self, servos: List[str], targets: List[int]) -> None:
        """
        MultiTarget Protocol: 0xAA, device number, 0x1F, number of targets, first channel number, first target
        low bits, first target high bits, second target low bits, second target high bits, …
        :param servos:
        :param targets:
        :return:
        """
        serial_cmd = chr(0xaa) + chr(0xC) + chr(0x1F) + chr(len(servos)) + chr(
            int(self.servo_robot_anatomy_map.get(servos[0])))
        for t in targets:
            serial_cmd += chr(t & 0x7F)
            serial_cmd += chr((t >> 7) & 0x7F)
        self.servo_controller.write(serial_cmd.encode('utf-8'))
        sleep(0.05)

    def forward(self):
        # < 6000 on channel 1
        self.motor_velocity_counter -= self.motor_step_size
        if self.motor_velocity_counter < self.servo_min:
            self.motor_velocity_counter = self.servo_min
        if self.motor_velocity_counter > self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_servo("motors", self.motor_velocity_counter)

    def reverse(self):
        # > 6000 on channel 1
        self.motor_velocity_counter += self.motor_step_size
        if self.motor_velocity_counter > self.servo_max:
            self.motor_velocity_counter = self.servo_max
        if self.motor_velocity_counter < self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_servo("motors", self.motor_velocity_counter)
        pass

    def STOPDROPANDROLL(self):
        # 6000 on channel 2 and 1
        # need to slowdown first!!
        while self.motor_turn_velocity_counter != self.servo_neutral:
            if self.motor_turn_velocity_counter > self.servo_neutral:
                self.motor_turn_velocity_counter -= self.motor_step_size
            else:
                self.motor_turn_velocity_counter += self.motor_step_size
            self.drive_servo("turn_motors", self.motor_velocity_counter)
        while self.motor_velocity_counter != self.servo_neutral:
            if self.motor_velocity_counter > self.servo_neutral:
                self.motor_velocity_counter -= self.motor_step_size
            else:
                self.motor_velocity_counter += self.motor_step_size
            self.drive_servo("motors", self.motor_velocity_counter)  # changed from turn_motors
        print("stopped")
        return

    def turn_waist(self, turn_right: bool):
        # channel 0
        # from right to left 4096, 4688, 5376, 5968, 8192
        if turn_right:
            self.twist_position += 1
        else:
            self.twist_position -= 1

        if self.twist_position < 0:
            self.twist_position = 0
        if self.twist_position > 4:
            self.twist_position = 4
        self.drive_servo("waist", self.five_steps_of_POWER[self.twist_position])

    def head_nod(self, turnip: bool):
        # channel 3
        # from right to left 4096, 4688, 5376, 5968, 8192
        if turnip:
            self.head_nod_pos += 1
        else:
            self.head_nod_pos -= 1

        if self.head_nod_pos < 0:
            self.head_nod_pos = 0
        if self.head_nod_pos > 4:
            self.head_nod_pos = 4
        self.drive_servo("head_tilt", self.five_steps_of_POWER[self.head_nod_pos])
        pass

    def head_shake(self, turn_right: bool):
        # channel 4
        # from up to down 4096, 4688, 5376, 5968, 8192
        if turn_right:
            self.head_pan_pos += 1
        else:
            self.head_pan_pos -= 1

        if self.head_pan_pos < 0:
            self.head_pan_pos = 0
        if self.head_pan_pos > 4:
            self.head_pan_pos = 4
        self.drive_servo("head_pan", self.five_steps_of_POWER[self.head_pan_pos])

    def left_drive_servos(self):
        # > 6000 on channel 2
        self.drive_servo("motors", self.servo_neutral)
        _serial_cmd = chr(0xaa) + chr(0xC) + chr(0x1F) + chr(0x02) + chr(0x01) + chr((6000 & 0x7F)) + chr(
            (6000 >> 7) & 0x7F) + chr((6000 & 0x7F)) + chr((6000 >> 7) & 0x7F)
        self.servo_controller.write(_serial_cmd.encode('utf-8'))
        # sleep(1)
        self.motor_turn_velocity_counter += self.motor_step_size
        if self.motor_velocity_counter > self.servo_max:
            self.motor_velocity_counter = self.servo_max
        if self.motor_velocity_counter < self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_multiple_servos(["motors", "turn_motors"],
                                   [self.servo_neutral, self.motor_turn_velocity_counter])
        # print(f"drive left with target {self.motor_turn_velocity_counter}")
        # sleep(0.05)

    def right_drive_servos(self):
        # < 6000 on channel 2
        self.drive_servo("motors", self.servo_neutral)
        self.motor_turn_velocity_counter -= self.motor_step_size
        if self.motor_velocity_counter < self.servo_min:
            self.motor_velocity_counter = self.servo_min
        if self.motor_velocity_counter > self.servo_neutral:
            self.motor_velocity_counter = self.servo_neutral
        self.drive_multiple_servos(["motors", "turn_motors"],
                                   [self.servo_neutral, self.motor_turn_velocity_counter])
        # print(f"drive right with target {self.motor_turn_velocity_counter}")
        # sleep(0.05)

    def right_drive_servos_beta(self, target: int) -> None:  # TODO: test this method. Also... adding the neut() to fwd/bkwd might solve the false start issues???
        # < 6000 on channel 2
        self.drive_servo("motors", self.servo_neutral)
        while self.motor_turn_velocity_counter <= target:
            self.motor_turn_velocity_counter -= self.motor_step_size
            if self.motor_velocity_counter < self.servo_min:
                self.motor_velocity_counter = self.servo_min
            if self.motor_velocity_counter > self.servo_neutral:
                self.motor_velocity_counter = self.servo_neutral
            self.drive_multiple_servos(["motors", "turn_motors"],
                                       [self.servo_neutral, self.motor_turn_velocity_counter])
            sleep(0.05)

    def reset_joints(self) -> None:
        for servo_motor in controller.servo_robot_anatomy_map.keys():
            controller.drive_servo(servo_motor, controller.servo_neutral)
            print(f"{servo_motor} set to neutral position")
            sleep(0.05)

    def left_arm(self, move_up_bool: bool) -> None:
        if move_up_bool:
            self.left_arm_position = 1
            self.drive_servo("l_shoulder", self.five_steps_of_POWER[0])
        if not move_up_bool:
            self.left_arm_position = 0
            self.drive_servo("l_shoulder", self.five_steps_of_POWER[4])

    def right_arm(self, move_up_bool: bool) -> None:
        if move_up_bool:
            self.left_arm_position = 1
            self.drive_servo("r_shoulder", self.five_steps_of_POWER[0])
        if not move_up_bool:
            self.left_arm_position = 0
            self.drive_servo("r_shoulder", self.five_steps_of_POWER[4])


if __name__ == '__main__':
    controller: Controller = Controller()
    for servo in controller.servo_robot_anatomy_map.keys():
        controller.drive_servo(servo, controller.servo_neutral)
        print(f"{servo} set to neutral position")
        sleep(0.05)
    try:
        for _ in range(0, 35):
            controller.right_drive_servos()
        sleep(1)
        controller.STOPDROPANDROLL()
        sleep(4)
        for _ in range(0, 35):
            controller.left_drive_servos()
        sleep(1)
    finally:
        controller.STOPDROPANDROLL()
