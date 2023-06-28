from abc import ABC, abstractmethod
from enum import Enum


class Height(Enum):
    SHORT = 1
    MEDIUM = 2
    TALL = 3


class Weight(Enum):
    LIGHT = 1
    MEDIUM = 2
    HEAVY = 3

class Age(Enum):
    YOUNG = 1
    ADULT = 2
    OLD = 3

class Human(ABC):

    def __init__(self, name, age, height, weight):
        self.age = age
        self.weight = weight
        self.height = height
        self.name = name

    def __str__(self):
        return self.name


class Specification(ABC):

    @abstractmethod
    def is_satisfied(self, item): pass

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)


class AgeSpecification(Specification):

    def __init__(self, age):
        self.age = age

    def is_satisfied(self, item):
        return item.age == self.age


class WeightSpecification(Specification):

    def __init__(self, weight):
        self.weight = weight

    def is_satisfied(self, item):
        return item.weight == self.weight


class HeightSpecification(Specification):

    def __init__(self, height):
        self.height = height

    def is_satisfied(self, item):
        return item.height == self.height


class Filter:

    @abstractmethod
    def filter(self, items, spec):
        pass


class BetterFilter(Filter):

    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item


class AndSpecification(Specification):

    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(map(lambda spec: spec.is_satisfied(item), self.args))
        # return all([spec.is_satisfied(item) for spec in self.args])


Jarry = Human('Jerry', Age.OLD, Height.TALL, Weight.MEDIUM)
Lasly = Human('Lasly', Age.YOUNG, Height.TALL, Weight.LIGHT)
Siera = Human('Siera', Age.ADULT, Height.MEDIUM, Weight.MEDIUM)
John = Human('John', Age.ADULT, Height.TALL, Weight.MEDIUM)
Grace = Human('Grace', Age.ADULT, Height.MEDIUM, Weight.LIGHT)


class OrSpecification(Specification):

    def __init__(self, *specs):
        self.specs = specs

    def is_satisfied(self, item):
        return any(map(lambda spec: spec.is_satisfied(item), self.specs))


humans = [Jarry, Lasly, Siera, John, Grace]

age_spec = AgeSpecification(Age.ADULT)
bf = BetterFilter()

weight_age_spec = age_spec | WeightSpecification(Weight.MEDIUM)
for man in bf.filter(humans, weight_age_spec):
    print(man)
