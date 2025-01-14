# -*- coding: utf-8 -*-
from typing import List
from src.dto import EventCountRequest
from .base_observer import InterfaceObserver


class SubjectEventCount:
    def __init__(self):
        self._observers: List[InterfaceObserver] = []

    def register_observer(self, observer: InterfaceObserver) -> None:
        self._observers.append(observer)

    def unregister_observer(self, observer: InterfaceObserver) -> None:
        self._observers.remove(observer)

    def notify_observers(self, data: List[EventCountRequest], filial_id: int) -> None:
        for observer in self._observers:
            observer.update(data, filial_id)
