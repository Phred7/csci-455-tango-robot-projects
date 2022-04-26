from random import random


class IdRatherRipMyNailOFF:

    def __int__(self):
        self.currentCoords = self.initial_coords()
        self.nextCoords = (0, 0)
        self.health = 400
        self.damage = 1  # might not use this, depends on how fast we want 'battles' to happen
        self.armor = 0  # might not use this, use with simple factorial equation to mitigate damage (dmg-x/100)
        self.enemyCount = 0
        self.battleFlag = False
        self.enemyDamage = 1

    def initial_coords(self):
        return (0, 0)

    def start_battle(self, difficulty):
        # i thought about doing classes for these but it might be easier to just do methods
        self.battleFlag = True
        enemyMax = 6
        if difficulty == 'medium':
            enemyMax = 10
        elif difficulty == 'hard':
            enemyMax = 15
        self.enemyCount = random.random(enemyMax)

    def attack_calc(self):  # not sure if this goes here or in controller
        if self.battleFlag:
            if self.enemyCount > 0:
                self.enemyCount -= self.damage  # using dynamic damage lets us just fill up features later
                for i in range(self.enemyCount):
                    self.health -= self.enemyDamage - (
                        self.armor)  # something like this for armor, might not be used
            if self.health < 1:
                print('you stupid loser idiot haha')  # should never happen unless you really suck at the game
            if self.enemyCount < 0 or not self.battleFlag:
                self.enemyCount = 0
                self.battleFlag = False
                print('battle win')  # placeholder, do callback to something here

    def recharge_station(self):
        self.health = 400
        print('recharged health i guess')

    def signal_station(self):
        pass
        # depending on how node layout is we could either just have some value range determine a direction
        # or we can just figure something else out. This does nothing for now though

    def fun_node(self):
        fun_choices = ['die', 'heal', 'armor', 'nothing', 'lore']
        choice = fun_choices[random.random(len(fun_choices) - 1)]

        if choice == 'die':
            self.health = 0
            print('you\'re dead roll better next time')
            # do exit stuff here
        elif choice == 'heal':
            self.health = 400
            print('healed health')
        elif choice == 'armor':
            self.armor += 1
            print('armor armored')
        elif choice == 'lore':
            print('lore placeholder')
            # read a lore document. Not sure if TTS can just do file inputs
        else:
            print('nothing happened.\nL')

    def trick_node(self):
        resp = input('this is the riddle question')
        if resp is not 'correct':
            self.health = 0
            print('you died wrong answer')
        else:
            print('you are correct good job')
            #maybe include some sort of score if we're feeling extra

    def on_finish(self): #note we don't need the key for this to work
        print('you finished')