from abc import ABC, abstractmethod


class BaseTable(ABC):

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def query(self):
        pass


class BaseFunc(ABC):

    def __init__(self, genner, handler) -> None:
        self.genner = genner
        self.handler = handler

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def query(self):
        pass
