import abc

class Shape(metaclass=abc.ABCMeta):
    """形状抽象类"""
    @abc.abstractmethod
    def draw(self): pass

class Rectangle(Shape):
    """正方形"""
    def draw(self):
        print('Inside Rectangle::draw() method.')

class Square(Shape):
    """方形"""
    def draw(self):
        print('Inside Square::draw() method.')

class Circle(Shape):
    """圆形"""
    def draw(self):
        print('Inside Circle::draw() method.')

class Color(metaclass=abc.ABCMeta):
    """颜色抽象类"""
    @abc.abstractmethod
    def fill(self): pass

class Red(Color):
    """红色"""
    def fill(self):
        print('Inside Red::fill() method.')


class Green(Color):
    """绿色"""
    def fill(self):
        print('Inside Green::fill() method.')


class Blue(Color):
    """蓝色"""
    def fill(self):
        print('Inside Blue::fill() method.')

class AbstractFactory(metaclass=abc.ABCMeta):
    """抽象工厂"""
    @abc.abstractmethod
    def get_color(self, color: str) -> Color: pass

    @abc.abstractmethod
    def get_shape(self, shpae: str) -> Shape: pass


class ShapeFactory(AbstractFactory):
    """形状工厂"""

    def get_shape(self, shape: str) -> Shape:
        if not shape:
            return None
        elif shape == 'Rectangle':
            return Rectangle()
        elif shape == 'Square':
            return Square()
        elif shape == 'Circle':
            return Circle()

    def get_color(self, color: str) -> Color:
        return None

class ColorFactory(AbstractFactory):
    """颜色工厂"""

    def get_shape(self, shpae: str) -> Shape:
        return None

    def get_color(self, color: str) -> Color:
        if not color:
            return None
        elif color == 'Red':
            return Red()
        elif color == 'Green':
            return Green()
        elif color == 'Blue':
            return Blue()

class FactoryProducer:
    """工厂创造器"""
    @staticmethod
    def get_factory(choice: str) -> AbstractFactory:
        if not choice:
            return None
        elif choice == 'Shape':
            return ShapeFactory()
        elif choice == 'Color':
            return ColorFactory()


shape_factory = FactoryProducer.get_factory('Shape')
color_factory = FactoryProducer.get_factory('Color')

circle = shape_factory.get_shape('Circle')
circle.draw()
square = shape_factory.get_shape('Square')
square.draw()
rectangle = shape_factory.get_shape('Rectangle')
rectangle.draw()

red = color_factory.get_color('Red')
red.fill()
green = color_factory.get_color('Green')
green.fill()
blue = color_factory.get_color('Blue')
blue.fill()