# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC


class IAdapterTask(ABC):
    @abstractmethod
    def process(self):
        raise NotImplementedError("Method not implemented")
