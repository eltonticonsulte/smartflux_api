# -*- coding: utf-8 -*-
from ..dto import CountEventDTO
from ..database import EventCountTemp


class CountEventMapper:
    @staticmethod
    def to_dto(count_event: EventCountTemp) -> CountEventDTO:
        return CountEventDTO(
            channel_id=count_event.channel_id,
            event_time=count_event.event_time,
            count_in=count_event.count_in,
            count_out=count_event.count_out,
            camera_id=count_event.camera_id,
        )

    @staticmethod
    def to_entity(count_event: CountEventDTO) -> EventCountTemp:
        return EventCountTemp(
            channel_id=count_event.channel_id,
            event_time=count_event.event_time,
            count_in=count_event.count_in,
            count_out=count_event.count_out,
            camera_id=count_event.camera_id,
        )
