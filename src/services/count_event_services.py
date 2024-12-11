# -*- coding: utf-8 -*-
from ..repository import CounterEventRepository
from typing import List
from ..dto import CountEventDTO, PullCountEventDTO


class CountEventServices:
    def __init__(self, repo: CounterEventRepository):
        self.repo = repo

    def add(self, data: PullCountEventDTO) -> List[CountEventDTO]:
        return self.repo.add_all(data.events)
