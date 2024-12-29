# -*- coding: utf-8 -*-
from ..dto import EventCountRequest
from ..database import EventCountTemp


class CountEventMapper:
    @staticmethod
    def to_dto(count_event: EventCountTemp) -> EventCountRequest:
        return EventCountRequest(
            channel_id=count_event.channel_id,
            event_time=count_event.event_time,
            count_in=count_event.count_in,
            count_out=count_event.count_out,
            camera_id=count_event.camera_id,
        )

    @staticmethod
    def create_event_request_to_entity(
        count_event: EventCountRequest,
    ) -> EventCountTemp:
        return EventCountTemp(
            channel_id=count_event.channel_id,
            event_time=count_event.event_time,
            count_in=count_event.count_in,
            count_out=count_event.count_out,
            camera_id=count_event.camera_id,
        )
