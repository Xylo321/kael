import abc


class Game(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def initialize(self):
        raise NotImplemented

    @abc.abstractmethod
    def startPlay(self):
        raise NotImplemented

    @abc.abstractmethod
    def endPlay(self):
        raise NotImplemented

    def play(self):
        self.initialize()
        self.startPlay()
        self.endPlay()


class Cricket(Game):
    def initialize(self):
        print('Cricket Game Initialized! Start playing.')

    def startPlay(self):
        print('Cricket Game Started. Enjoy the game!')

    def endPlay(self):
        print('Cricket Game Finished!')


class Football(Game):
    def initialize(self):
        print('Football Game Initialized! Start playing.')

    def startPlay(self):
        print('Football Game Started. Enjoy the game!')

    def endPlay(self):
        print('Football Game Finished!')


game = Cricket()
game.play()

game = Football()
game.play()