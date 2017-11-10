from abc import ABCMeta, abstractmethod

ABC = ABCMeta('ABC', (object,), {'__slots__': ()})

class GeometryModel(ABC):

    @abstractmethod
    def from_k_points(self):
        pass

    @abstractmethod
    def get_projections(self):
        pass
