# -*- coding: utf-8 -*-

from .base_repository import BaseRepository
from ..database import EventCountTemp, DBConnectionHandler
from ..dto import CountEventDTO
from ..mappers import CountEventMapper


class CounterEventRepository(BaseRepository):
    def __init__(self):
        pass

    def add(self, data: CountEventDTO) -> int:

        with DBConnectionHandler() as session:
            camera = (
                session.query(EventCountTemp)
                .filter(EventCountTemp.channel_id == data.channel_id)
                .first()
            )
            data.camera_id = camera.camera_id

        entity = CountEventMapper.to_entity(data)
        super().add(entity)
