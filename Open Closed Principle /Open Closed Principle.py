# https://www.youtube.com/watch?v=vU-iw-Fnwzg
from abc import ABC, abstractmethod
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    ORANGE = 4


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    def __init__(self, name, color, size):
        self.size = size
        self.name = name
        self.color = color

    def __str__(self):
        return self.name


class ProductFilter:

    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color:
                yield p

    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size:
                yield p



# Паттерн Спецификация
class Specification(ABC):

    @abstractmethod
    def is_satisfied(self, item):
        pass

    def __and__(self, other):
        return AndSpecification(self, other)


class Filter(ABC):

    @abstractmethod
    def filter(self, items, spec):
        pass


class ColorSpecification(Specification):

    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color


class SizeSpecification(Specification):

    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size


# Комбинатор
class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(map(  # медленнее, но эффективнее по памяти
            lambda spec: spec.is_satisfied(item), self.args
        ))
        #return all([spec.is_satisfied(item) for spec in self.args])  # быстрее, но по памяти менее эффективнее, так как больше памяти занимает


class BetterFilter(Filter):

    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item


if __name__ == '__main__':
    apple = Product('Apple', Color.GREEN, Size.SMALL)
    tree = Product('Tree', Color.GREEN, Size.LARGE)
    house = Product('House', Color.BLUE, Size.LARGE)

    products = [apple, tree, house]

    pf = ProductFilter()
    print('Green products (old):')
    for p in pf.filter_by_color(products, Color.GREEN):
        print(f' - {p.name} is green')

    bf = BetterFilter()
    print('Green products (new):')
    green = ColorSpecification(Color.GREEN)
    for p in bf.filter(products, green):
        print(f' - {p.name} is green')

    print('Large products:')
    large = SizeSpecification(Size.LARGE)
    for p in bf.filter(products, large):
        print(f' - {p.name} is large')

    print('Large blue items:')
    # large_blue = AndSpecification(large, ColorSpecification(Color.BLUE))
    large_blue = SizeSpecification(Size.LARGE) & ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_blue):
        print(f' - {p.name} is large and blue')