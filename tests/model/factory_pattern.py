import abc

class Shape(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def draw(self): pass

class Rectangle(Shape):
    def draw(self):
        print('Inside Rectangle::draw() method.')

class Square(Shape):
    def draw(self):
        print('Inside Square::draw() method.')

class Circle(Shape):
    def draw(self):
        print('Inside Circle::draw() method.')

class ShapeFactory:
    def get_shape(self, shape_type):
        if shape_type:
            if shape_type == 'Rectangle':
                return Rectangle()
            elif shape_type == 'Square':
                return Square()
            elif shape_type == 'Circle':
                return Circle()
        else:
            return None

shape_factory = ShapeFactory()

obj = shape_factory.get_shape('Rectangle')
obj.draw()

obj = shape_factory.get_shape('Square')
obj.draw()

obj = shape_factory.get_shape('Circle')
obj.draw()
