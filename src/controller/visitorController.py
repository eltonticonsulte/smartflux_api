# -*- coding: utf-8 -*-
from fastapi import APIRouter, status
from ..dto import PullCountEventDTO, CountEventDTO
from ..services import CountEventServices


class CounterEventController:
    def __init__(self, service: CountEventServices):
        self.service = service

    async def register_event(self, data: PullCountEventDTO):
        pass
