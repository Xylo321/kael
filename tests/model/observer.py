import abc


class Subject:
    """定义一个主题

    """
    def __init__(self):
        self._state = None
        self._observers = set()

    @property
    def observers(self):
        return self._observers

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        self.notify_all_observers()

    @state.deleter
    def state(self):
        del self._state

    def attach(self, observer):
        self.observers.add(observer)

    def notify_all_observers(self):
        for observer in self.observers:
            observer.update()


class Observer(metaclass=abc.ABCMeta):
    """定义一个观察者抽象类

    """
    def __init__(self, subject: Subject):
        self._subject = subject

    @property
    def subject(self):
        return self._subject

    @abc.abstractmethod
    def update(self):
        pass


class BinaryObserver(Observer):
    """定义一个二进制观察者

    """
    def update(self):
        print('Binary String:', self.subject.state)

    def __init__(self, subject: Subject):
        super().__init__(subject)
        # 为这个主题二进制观察者
        self.subject.attach(self)


class OctalObserver(Observer):
    """定义一个8进制观察者

    """
    def __init__(self, subject: Subject):
        super().__init__(subject)
        self.subject.attach(self)

    def update(self):
        print('Octal String:', self.subject.state)


class HexObserver(Observer):
    """定义一个16进制观察者

    """
    def __init__(self, subject: Subject):
        super().__init__(subject)
        self.subject.attach(self)

    def update(self):
        print('Hex String:', self.subject.state)


subject = Subject()

HexObserver(subject)
OctalObserver(subject)
BinaryObserver(subject)

print('First state change: 15')
subject.state = 15
print('Second state change: 10')
subject.state = 10