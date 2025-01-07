# -*- coding: utf-8 -*-
from src.interfaces.services import InterfaceTaskUpdateViewService
from ..database import EventCount
from ..repository import (
    TaskUpdateViewRepository,
    CountEventStorageRepository,
    CountEventRepository,
)


class TaskUpdateViewService(InterfaceTaskUpdateViewService):
    def __init__(
        self,
        repo_view: TaskUpdateViewRepository,
        repo_storage: CountEventStorageRepository,
        repo_event: CountEventRepository,
    ):
        self.repo_view = repo_view
        self.repo_storage = repo_storage
        self.repo_event = repo_event

    def update_view(self):
        agregates = self.repo_view.fetch_aggregate()
        result_channel_ids = [agre.channel_id for agre in agregates]

        event_counts = [
            EventCount(
                channel_id=agre.channel_id,
                date=agre.hour_timestamp.date(),
                hour=agre.hour_timestamp.hour,
                total_count_in=agre.total_count_in,
                total_count_out=agre.total_count_out,
                filial_id=agre.filial_id,
                zona_id=agre.zone_id,
                zone_name=agre.zone_name,
            )
            for agre in agregates
        ]

        self.repo_storage.create_all(event_counts)
        self.repo_event.delete_by_channel_ids(result_channel_ids)
