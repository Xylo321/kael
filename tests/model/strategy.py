import abc


class Strategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def doOperation(self, num1: int, num2: int) -> int:
        pass


class OperationAdd(Strategy):
    def doOperation(self, num1: int, num2: int) -> int:
        return num1 + num2


class OperationSubstract(Strategy):
    def doOperation(self, num1: int, num2: int) -> int:
        return num1 - num2


class OperationMultiply(Strategy):
    def doOperation(self, num1: int, num2: int) -> int:
        return num1 * num2


class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def execute_strategy(self, num1: int, num2: int) -> int:
        return self._strategy.doOperation(num1, num2)


context = Context(OperationAdd())
print('10 + 5 =', context.execute_strategy(10, 5))

context = Context(OperationSubstract())
print('10 - 5 =', context.execute_strategy(10, 5))

context = Context(OperationMultiply())
print('10 * 5 =', context.execute_strategy(10, 5))