import speech_recognition as sr
import tkinter

from controller import Controller
#from controller import Controller on the robot's code


class VoiceInput:

    def __init__(self) -> None:
        self.robot_controller: Controller = Controller()
        self.window = tkinter.Tk()

    def drive_robot(self) -> None:
        listening = True
        while listening:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dyanmic_energythreshhold = 3000
                # r.operation_timeout = 8
                # r.phrase_threshold = 0.15

                try:
                    print("listening")
                    audio = r.listen(source, timeout=8)
                    print("Got audio")
                    userInput = r.recognize_google(audio)
                    print(userInput)
                    arrayofwords = userInput.split()
                    if 'stop' in arrayofwords or 'die' in arrayofwords or 'kill' in arrayofwords or ("oh" in arrayofwords and "my" in arrayofwords and "god" in arrayofwords) or ("my" in arrayofwords and "god" in arrayofwords):
                        # "stop": stop
                        self.robot_controller.STOPDROPANDROLL()
                    elif ('head' in arrayofwords and 'up' in arrayofwords) or ('had' in arrayofwords and 'up' in arrayofwords):
                        # "head", "up": head up
                        self.robot_controller.headnod(True)
                    elif ('head' in arrayofwords and 'down' in arrayofwords) or ('had' in arrayofwords and 'up' in arrayofwords):
                        # "head", "down": head down
                        self.robot_controller.headnod(False)
                    elif ('head' in arrayofwords and 'left' in arrayofwords) or ('had' in arrayofwords and 'up' in arrayofwords):
                        # "head", "left": head left
                        self.robot_controller.headshake(False)
                    elif ('head' in arrayofwords and 'right' in arrayofwords) or ('had' in arrayofwords and 'up' in arrayofwords):
                        # "head", "right": head right
                        self.robot_controller.headshake(True)
                    elif 'waist' in arrayofwords and 'left' in arrayofwords:
                        # "waist", "left": waist left
                        self.robot_controller.turn_waist(False)
                    elif 'waist' in arrayofwords and 'right' in arrayofwords:
                        # "waist", "right": waist right
                        self.robot_controller.turn_waist(True)
                    elif 'forward' in arrayofwords or ('forward' in arrayofwords and 'body' in arrayofwords):
                        # "forward", or "body", "forward": forward
                        self.robot_controller.forward()
                    elif 'backwards' in arrayofwords or ('backwards' in arrayofwords and 'body' in arrayofwords) or 'backward' in arrayofwords:
                        # "backwards",or "body", "backwards": backwards
                        self.robot_controller.reverse()
                    elif 'left' in arrayofwords or ('left' in arrayofwords and 'body' in arrayofwords):
                        # "left", or "body", "left": left
                        self.robot_controller.left_drive_servos()
                    elif 'right' in arrayofwords or ('right' in arrayofwords and 'body' in arrayofwords):
                        # "right", or "body", "right": right
                        self.robot_controller.right_drive_servos()
                    elif 'favorite' in arrayofwords:
                        print("Connie, obviously")


                except sr.UnknownValueError:
                    print("Don't knoe that werd")
                except sr.WaitTimeoutError:
                    print("Listen timeout exceeded")
        pass

if __name__ == '__main__':
    voice_input: VoiceInput = VoiceInput()
    voice_input.drive_robot()
