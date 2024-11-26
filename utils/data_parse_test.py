# -*- coding: utf-8 -*-
import unittest
import logging
from .data_parse import DataParse


class TestDataParseInit(unittest.TestCase):
    def setUp(self) -> None:
        self.log = logging.getLogger(__name__)

    def test_dual_key(self):
        data = {"key": "value", "key2": "value2"}

        class Data(DataParse):
            def __init__(self, data: dict) -> None:
                super().__init__(data)
                self.key = self.parse("key3 | key2", str)

        dp = Data(data)

        self.assertEqual(dp.key, "value2")

    def test_dual_key_order_load(self):
        data = {"key3": "value", "key2": "value2"}

        class Data(DataParse):
            def __init__(self, data: dict) -> None:
                super().__init__(data)
                self.key = self.parse("key3 | key2", str)

        dp = Data(data)

        self.assertEqual(dp.key, "value")

    def test_init_with_dict(self):
        data = {"key": "value"}
        dp = DataParse(data)
        self.assertIsInstance(dp, DataParse)
        self.assertEqual(dp.data, data)

    def test_init_with_non_dict(self):
        data = [1, 2, 3]
        with self.assertRaises(AssertionError):
            DataParse(data)

    def test_parse_valid_value(self):
        data = {"key": "value"}
        parser = DataParse(data)
        assert parser.parse("key", str) == "value"

    def test_type_default(self):
        data = {"key": "value"}
        parser = DataParse(data)
        assert parser.parse("key", int, 0) == 0

    def test_parse_nonexistent_key(self):
        data = {"key": "value"}
        parser = DataParse(data)
        with self.assertRaises(ValueError):
            parser.parse("another_key", str)

    def test_parse_invalid_type(self):
        data = {"key": 1}
        parser = DataParse(data)
        with self.assertRaises(ValueError):
            parser.parse("key", str)

    def test_parse_default_value(self):
        data = {}
        parser = DataParse(data)
        assert parser.parse("key", str, "default") == "default"


if __name__ == "__main__":
    unittest.main()
