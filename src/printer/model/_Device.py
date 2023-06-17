from abc import (
    ABCMeta,
    abstractmethod,
)


class Device(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_status(self) -> int:
        raise NotImplementedError()
