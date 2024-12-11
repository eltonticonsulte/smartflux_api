# -*- coding: utf-8 -*-
from typing import List
from .base_repository import BaseRepository
from ..database import EventCountTemp, DBConnectionHandler, Camera
from ..dto import CountEventDTO, CameraDTO
from ..mappers import CountEventMapper


class CounterEventRepository(BaseRepository):
    def __init__(self):
        pass

    def add_all(self, datas: List[CountEventDTO]) -> List[CountEventDTO]:
        data_success, datas_fail = self.check_chennel(datas)
        events = [CountEventMapper.to_entity(data) for data in data_success]
        self.add_all(events)
        return datas_fail

    def check_chennel(self, datas: List[CountEventDTO]) -> bool:
        cameras = self.get_all(Camera)
        datas_fail = []
        data_success = []
        tokens = [camera.channel_id for camera in cameras]
        for data in datas:
            if data.channel_id not in tokens:
                datas_fail.append(data)
            else:
                data_success.append(data)
        return data_success, datas_fail

    def add_all(self, events: List[EventCountTemp]):
        with DBConnectionHandler() as db:
            try:
                db.bulk_save_objects(events)
                db.commit()
            except Exception as error:
                db.rollback()
                raise error
