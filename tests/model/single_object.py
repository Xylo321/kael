class SingleObject:
    _instance = None

    def __init__(self):
        if SingleObject._instance != None:
            raise Exception()

    @staticmethod
    def get_single_object():
        try:
            SingleObject._instance = SingleObject()
            return SingleObject._instance
        except:
            return None

    def say(self):
        print('Hello.')

so = SingleObject.get_single_object()
so.say()

# so1 = SingleObject.get_single_object()
# so1.say()

so2 = SingleObject()
so2.say()