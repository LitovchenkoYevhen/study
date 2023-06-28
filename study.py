from abc import abstractmethod, ABC


class Chair(ABC):
    """
        Каждый отдельный продукт семейства продуктов должен иметь базовый интерфейс.
        Все вариации продукта должны реализовывать этот интерфейс.
    """

    @abstractmethod
    def has_legs(self): pass

    @abstractmethod
    def sit_on(self): pass


class ModernChair(Chair):

    def has_legs(self):
        print('Modern chair has legs')

    def sit_on(self):
        print('You can sit on Modern chair.')


class VictorianChair(Chair):

    def has_legs(self):
        print('Victorian chair has legs')

    def sit_on(self):
        print('You can sit on Victorian chair.')


class Table(ABC):
    """
        Базовый интерфейс другого продукта. Все продукты могут взаимодействовать
        друг с другом, но правильное взаимодействие возможно только между продуктами
        одной и той же конкретной вариации.
    """

    @abstractmethod
    def has_box(self) -> None:
        """
            Продукт B способен работать самостоятельно...
        """
        pass

    @abstractmethod
    def can_store_items(self, collaorator: Chair) -> None:
        """
            ...а также взаимодействовать с Продуктами A той же вариации.

            Абстрактная Фабрика гарантирует, что все продукты, которые она создает,
            имеют одинаковую вариацию и, следовательно, совместимы.
        """
        pass


class ModernTable(Table):

    def has_box(self):
        print('Has modern box')

    def can_store_items(self, collaborator: ModernChair):
        print('Can store modern items')


class VictorianTable(Table):

    def has_box(self):
        print('Has victorian box')

    def can_store_items(self, collaborator: VictorianChair):
        print('Здесь викторианский стол хорошо сочитается с викторианским стулом.')


class FurnitureFactory(ABC):
    """
        Интерфейс Абстрактной Фабрики объявляет набор методов, которые возвращают
        различные абстрактные продукты. Эти продукты называются семейством и связаны
        темой или концепцией высокого уровня. Продукты одного семейства обычно могут
        взаимодействовать между собой. Семейство продуктов может иметь несколько
        вариаций, но продукты одной вариации несовместимы с продуктами другой.
    """

    @abstractmethod
    def create_chair(self) -> Chair: pass

    @abstractmethod
    def create_table(self) -> Table: pass


class ModernFurnitureFactory(FurnitureFactory):
    """
        Конкретная Фабрика производит семейство продуктов одной вариации. Фабрика
        гарантирует совместимость полученных продуктов. Обратите внимание, что
        сигнатуры методов Конкретной Фабрики возвращают абстрактный продукт, в то
        время как внутри метода создается экземпляр конкретного продукта.
    """

    def create_chair(self) -> Chair:
        return ModernChair()

    def create_table(self) -> Table:
        return ModernTable()


class VictorianFurnitureFactory(FurnitureFactory):
    """
        Каждая Конкретная Фабрика имеет соответствующую вариацию продукта.
    """

    def create_chair(self) -> Chair:
        return VictorianChair()

    def create_table(self) -> Table:
        return VictorianTable()

