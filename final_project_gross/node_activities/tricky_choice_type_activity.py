from controller_interface import ControllerInterface
from node_activity import NodeActivity
from player_statistics import PlayerStatistics
from speech import Speech


class TrickyChoiceTypeActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics, controller_interface: ControllerInterface) -> None:
        NodeActivity.__init__(self, player_statistics, controller_interface)

    def node_activity(self) -> None:
        # updates kivy graphics
        with open('images/picture.txt', "w") as f:
            f.write('images/tricky.jpeg')

        # T\ODO: replace input with Speech.get_speech()
        output = "If you were a graduating senior, which four hundred level elective should you avoid?"
        Speech.say(output)
        resp = ''
        resp = Speech.get_speech()
        if 'four fifty five' in resp or 'four hundred and fifty five' in resp or 'robotics' in resp or '455' in resp:
            self.controller_interface.head_up()
            sleep(1)
            self.controller_interface.head_down()
            sleep(1)
            self.player_statistics.set_damage(455)
            Speech.say('you are correct good job. Your damage has been set to four hundred and fifty five.')
            # T\ODO: maybe include some sort of score if we're feeling extra spicy - we are not
        else:
            self.player_statistics.set_health(0)
            Speech.say('you died wrong answer')
            # TODO: make dead state and game exit

