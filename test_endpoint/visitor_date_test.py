# -*- coding: utf-8 -*-
import unittest
from fastapi.testclient import TestClient
from main import app
from .visitor_base import BaseTestEndpointDate


class TestVisitorEndpointDate(BaseTestEndpointDate):
    def test_date_with_start_date(self):
        params = {"start_date": "2025-02-26"}
        response = self.client.get(
            "/v1/visitor/date",
            headers={"Authorization": f"Bearer {self.token}"},
            params=params,
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        print(result)
        self.assertIsNotNone(response.json())
        self.validate_date_response(result)
        table = result.get("table")
        values = table[0]
        self.validate_date_formate(values.get("date"), "%Y-%m-%d %H:%M")

    def test_invalid_period_data(self):
        params = {"start_date": "2025-02-27", "end_date": "2025-02-26"}
        response = self.client.get(
            "/v1/visitor/date",
            headers={"Authorization": f"Bearer {self.token}"},
            params=params,
        )
        self.assertEqual(response.status_code, 500)
        self.assertIsNotNone(response.json())

    def test_date_with_start_and_end_date(self):
        params = {"start_date": "2025-02-26", "end_date": "2025-02-27"}
        response = self.client.get(
            "/v1/visitor/date",
            headers={"Authorization": f"Bearer {self.token}"},
            params=params,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.validate_date_response(response.json())

    def test_date_with_zone(self):
        params = {"start_date": "2025-02-26", "zone": "Elev. Norte"}
        response = self.client.get(
            "/v1/visitor/date",
            headers={"Authorization": f"Bearer {self.token}"},
            params=params,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())


if __name__ == "__main__":
    unittest.main()
