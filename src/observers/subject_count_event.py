# -*- coding: utf-8 -*-
from typing import List
from logging import getLogger
from src.dto import EventCountRequest
from src.interfaces import InterfaceObserver


class SubjectEventCount:
    def __init__(self):
        self.log = getLogger(__name__)
        self._observers: List[InterfaceObserver] = []

    def register_observer(self, observer: InterfaceObserver) -> None:
        self._observers.append(observer)

    def unregister_observer(self, observer: InterfaceObserver) -> None:
        self._observers.remove(observer)

    async def notify_observers(
        self, data: List[EventCountRequest], filial_id: int
    ) -> None:
        self.log.info(f"Notifying observers... {len(self._observers)}")
        count = 0
        for observer in self._observers:
            self.log.info(f"Notifying observer: {observer}")
            await observer.update(data, filial_id)
            count += 1
        self.log.info(f"Notified {count} observers")
