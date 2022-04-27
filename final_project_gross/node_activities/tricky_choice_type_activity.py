from node_activity import NodeActivity
from player_statistics import PlayerStatistics


class TrickyChoiceTypeActivity(NodeActivity):

    def __init__(self, player_statistics: PlayerStatistics) -> None:
        NodeActivity.__init__(self, player_statistics)

    def node_activity(self) -> None:
        # updates kivy graphics
        with open('images/picture.txt', "w") as f:
            f.write('images/tricky.jpeg')

        resp = input('this is the riddle question')  # TODO: replace input with Speech.get_speech()
        if resp is not 'correct':
            self.player_statistics.set_health(0)
            print('you died wrong answer')
        else:
            print('you are correct good job')
            # TODO: maybe include some sort of score if we're feeling extra spicy
