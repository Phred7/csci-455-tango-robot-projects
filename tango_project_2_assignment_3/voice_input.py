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

                try:
                    print("listening")
                    audio = r.listen(source)
                    print("Got audio")
                    userInput = r.recognize_google(audio)
                    print(userInput)
                    arrayofwords = userInput.split()
                    if 'head' in arrayofwords and 'up' in arrayofwords:
                        # "head", "up": head up
                        self.robot_controller.headnod(True)
                    elif 'head' in arrayofwords and 'down' in arrayofwords:
                        # "head", "down": head down
                        self.robot_controller.headnod(False)
                    elif 'head' in arrayofwords and 'left' in arrayofwords:
                        # "head", "left": head left
                        self.robot_controller.headshake(False)
                    elif 'head' in arrayofwords and 'right' in arrayofwords:
                        # "head", "right": head right
                        self.robot_controller.headshake(True)
                    elif 'waist' in arrayofwords and 'left' in arrayofwords:
                        # "waist", "left": waist left
                        self.robot_controller.turnwaist(False)
                    elif 'waist' in arrayofwords and 'right' in arrayofwords:
                        # "waist", "right": waist right
                        self.robot_controller.turnwaist(True)
                    elif 'forward' in arrayofwords or ('forward' in arrayofwords and 'body' in arrayofwords):
                        # "forward", or "body", "forward": forward
                        self.robot_controller.forward()
                    elif 'backwards' in arrayofwords or ('backwards' in arrayofwords and 'body' in arrayofwords):
                        # "backwards",or "body", "backwards": backwards
                        self.robot_controller.reverse()
                    elif 'left' in arrayofwords or ('left' in arrayofwords and 'body' in arrayofwords):
                        # "left", or "body", "left": left
                        self.robot_controller.left()
                    elif 'right' in arrayofwords or ('right' in arrayofwords and 'body' in arrayofwords):
                        # "right", or "body", "right": right
                        self.robot_controller.right()
                    elif 'stop' in arrayofwords:
                        # "stop": stop
                        self.robot_controller.STOPDROPANDROLL()

                except sr.UnknownValueError:
                    print("Don't knoe that werd")
        pass

if __name__ == '__main__':
    voice_input: VoiceInput = VoiceInput()
    voice_input.drive_robot()