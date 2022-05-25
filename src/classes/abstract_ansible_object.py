from abc import ABC
from abc import abstractmethod


class AnsibleObject(ABC):

    @property
    @abstractmethod
    def qualified_name():
        pass

    @property
    @abstractmethod
    def usage():
        pass

    @property
    @abstractmethod
    def description():
        pass

    @abstractmethod
    def __init__():
        pass
