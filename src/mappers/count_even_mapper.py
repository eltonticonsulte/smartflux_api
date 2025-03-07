# -*- coding: utf-8 -*-
from typing import Any, List, Tuple

from sqlalchemy import Row
from src.dto import RequestEventCount, EventCountDataValidate, RequestRegisterWebsocket
from src.database import EventCountTemp, WebsocketNotification


class CountEventMapper:
    @staticmethod
    def to_dto(count_event: EventCountTemp) -> RequestEventCount:
        return RequestEventCount(
            channel_id=count_event.channel_id,
            event_time=count_event.event_time,
            count_in=count_event.count_in,
            count_out=count_event.count_out,
            camera_id=count_event.camera_id,
        )

    @staticmethod
    def create_event_request_to_entity(
        count_event: RequestEventCount,
    ) -> EventCountTemp:
        return EventCountTemp(
            channel_id=count_event.channel_id,
            event_time=count_event.event_time,
            count_in=count_event.count_in,
            count_out=count_event.count_out,
        )

    @staticmethod
    def create_event_request_to_validate(
        event: RequestEventCount,
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
    def create_event_to_websocket(
        counts: List[Row[Tuple[int, int, Any]]],
        data: RequestRegisterWebsocket,
        capacity: int,
    ) -> WebsocketNotification:
        label = []
        count_in = []
        count_out = []
        total_in = 0
        total_out = 0
        for item in counts:
            label.append(item.label)
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            total_in += item.total_count_in
            total_out += item.total_count_out
        return WebsocketNotification(
            connect_id=data.connect_id,
            token_filial=data.token_filial,
            total_in=total_in,
            total_out=total_out,
            count_max_capacity=capacity,
            label=label,
            count_in=count_in,
            count_out=count_out,
        )
