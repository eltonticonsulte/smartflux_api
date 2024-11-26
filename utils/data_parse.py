# -*- coding: utf-8 -*-
from logging import getLogger


class DataParse:
    def __init__(self, data: dict) -> None:
        self.log = getLogger(__name__)
        assert isinstance(
            data, dict
        ), f"expected dict, received {type(data)} value {data}"
        self.data = data

    def parse(self, key: str, type_expected: type, default: any = None) -> any:
        if not "|" in key:
            return self._pars_key(key, type_expected, default)
        return self.multiplas_key(key, type_expected, default)

    def multiplas_key(self, key: str, type_expected: type, default: any = None) -> any:
        keys = key.split("|")
        for k in keys:
            value = self.data.get(k.strip())
            if value is None:
                continue
            return self._pars_key(k.strip(), type_expected, default)
        return self._pars_key(k.strip(), type_expected, default)

    def _pars_key(self, key: str, type_expected: type, default: any = None) -> any:
        value = self.data.get(key, default)
        if value is None:
            raise ValueError(f"not found {key} in {self.data}")

        if not isinstance(value, type_expected):
            value = default
            if not isinstance(value, type_expected):
                raise ValueError(
                    f"invalid type  for {key} {value}, expected {type_expected} got ({type(value)})"
                )
        if self.data.get(key) is None:
            self.log.warning(f"Cannot parse {key} using default {key}={default}")
        return value
