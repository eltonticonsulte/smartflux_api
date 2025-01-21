# -*- coding: utf-8 -*-
from src.dto import EventCountRequest, EventCountDataValidate, EventCountSendWebsocket
from src.database import EventCountTemp


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
        )

    @staticmethod
    def create_event_request_to_validate(
        event: EventCountRequest,
    ) -> EventCountDataValidate:
        return EventCountDataValidate(
            event_id=event.event_id,
            camera_name="",
            channel_id=event.channel_id,
            zone_name="",
            count_in=event.count_in,
            count_out=event.count_out,
            event_time=event.event_time,
            status=False,
            description="",
        )

    @staticmethod
    def create_event_validate_to_entity(
        validate: EventCountDataValidate,
    ) -> EventCountTemp:
        return EventCountTemp(
            channel_id=validate.channel_id,
            event_time=validate.event_time,
            count_in=validate.count_in,
            count_out=validate.count_out,
        )

    @staticmethod
    def create_event_validate_to_websocket(
        validate: EventCountDataValidate,
    ) -> EventCountSendWebsocket:
        return EventCountSendWebsocket(
            camera_name=validate.camera_name,
            zone_name=validate.zone_name,
            count_in=validate.count_in,
            count_out=validate.count_out,
            event_time=validate.event_time,
            description=validate.description,
        )
