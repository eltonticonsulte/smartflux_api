# -*- coding: utf-8 -*-
import unittest
from fastapi.testclient import TestClient
from main import app  # importe a sua aplicação FastAPI

from .visitor_base import BaseTestEndpointDate


class TestVisitorEndpointTotal(BaseTestEndpointDate):
    def test_total_with_date(self):
        params = {"date": "2025-02-27"}
        response = self.client.get(
            "/v1/visitor/total",
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_total_with_null_date(self):
        params = {"date": None}
        response = self.client.get(
            "/v1/visitor/total",
            params=params,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertIsNotNone(response.json())


if __name__ == "__main__":
    unittest.main()
