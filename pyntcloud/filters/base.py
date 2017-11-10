from abc import ABCMeta, abstractmethod

ABC = ABCMeta('ABC', (object,), {'__slots__': ()})

class Filter(ABC):
    """Base class for filters."""

    def __init__(self, pyntcloud):
        self.pyntcloud = pyntcloud

    @abstractmethod
    def extract_info(self):
        pass

    @abstractmethod
    def compute(self):
        pass
