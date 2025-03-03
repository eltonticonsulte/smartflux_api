# -*- coding: utf-8 -*-
from logging import getLogger
from src.interfaces import IAdapterTask
from src.database import CountMaximunCapacity
from src.repository import CapacityRepository, StorageTodayRepository, FilialRepository


class TaskCapacity(IAdapterTask):
    def __init__(
        self,
        rep_capacity: CapacityRepository,
        rep_today: StorageTodayRepository,
        rep_filial: FilialRepository,
    ):
        self.log = getLogger(__name__)
        self.rep_capacity = rep_capacity
        self.rep_today = rep_today
        self.rep_filial = rep_filial

    def process(self):
        all_filial = self.rep_filial.get_all()
        if len(all_filial) == 0:
            self.log.warning("Não há filiais cadastradas")
            return
        for filial in all_filial:
            count = self.compute_capacity(filial.filial_id)
            self.rep_capacity.update(
                CountMaximunCapacity(filial_id=filial.filial_id, count_maximun=count)
            )

    def compute_capacity(self, filial_id: int) -> int:
        counts = self.rep_today.count_by_filial(filial_id)
        if not isinstance(counts.total_count_in, int):
            self.log.warning(f"total_count_in is not int {counts.total_count_in}")
            return 0
        if not isinstance(counts.total_count_out, int):
            self.log.warning(f"total_count_out is not int {counts.total_count_out}")
            return 0
        total = abs(counts.total_count_in - counts.total_count_out)
        self.log.info(f"Capacity Filial {filial_id} {total}")

        return total if total > 0 else 0
