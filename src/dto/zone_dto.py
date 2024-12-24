# -*- coding: utf-8 -*-
from ..common import UserRole


class ZoneDTO:
    def __init__(
        self,
        name: str,
        filial_id: int,
    ):
        self.name = name
        self.filial_id = filial_id

    def __repr__(self):
        return f"ZoneDTO(name={self.name}, filial_id={self.filial_id})"
