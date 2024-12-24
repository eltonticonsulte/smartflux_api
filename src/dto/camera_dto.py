# -*- coding: utf-8 -*-
from ..common import UserRole


class CameraDTO:
    def __init__(
        self,
        channel_id: int,
        name: str,
        zona_id: int,
        metadate: dict,
    ):
        self.channel_id = channel_id
        self.name = name
        self.zona_id = zona_id
        self.metadate = metadate

    def __repr__(self):
        return f"ZoneDTO(channel_id={self.channel_id}, name={self.name}, zona_id={self.zona_id}, metadate={self.metadate})"
