# -*- coding: utf-8 -*-
import unittest
from fastapi.testclient import TestClient
from main import app  # importe a sua aplicação FastAPI

from .visitor_base import BaseTestEndpointDate


class TestVisitorEndpointReportGrup(BaseTestEndpointDate):
    def test_report_grup_with_start_date(self):
        params = {"start_date": "2025-02-26"}
        response = self.client.get(
            "/v1/visitor/report/grup",
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

    def test_report_grup_with_start_and_end_date(self):
        params = {"start_date": "2025-02-26", "end_date": "2025-02-27"}
        response = self.client.get(
            "/v1/visitor/report/grup",
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

    def test_report_grup_with_grup(self):
        params = {"start_date": "2025-02-26", "grup": "AUTO_SELECT"}
        response = self.client.get(
            "/v1/visitor/report/grup",
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)


if __name__ == "__main__":
    unittest.main()
