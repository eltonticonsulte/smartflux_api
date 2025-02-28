# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from fastapi.testclient import TestClient
from main import app


class BaseTestEndpointDate(unittest.TestCase):
    client = TestClient(app)
    response = client.post(
        "/v1/user/login", data={"username": "BelaVista", "password": "B123"}
    )
    if response.status_code != 200:
        raise Exception(response.json())
    data = response.json()
    token = data.get("access_token")

    def validate_date_formate(self, date_str: str, format: str = "%Y-%m-%d"):
        datetime.strptime(date_str, format)

    def validate_date_response(self, data: dict):
        label_input = "date"
        self.base_validate_date_response(data, label_input)

    def validate_code_response(self, data: dict):
        label_input = "code"
        self.base_validate_date_response(data, label_input)

    def base_validate_date_response(self, data: dict, label_input: str):
        table = data.get("table")
        self.assertTrue(isinstance(table, list))
        len_table = len(table)
        if len_table > 0:
            values = table[0]
            self.assertTrue(label_input in values)
            self.assertTrue("people_in" in values)
            self.assertTrue("people_out" in values)

        linegraph = data.get("linegraph")
        self.assertTrue(isinstance(linegraph, dict))
        self.assertTrue("label" in linegraph)
        self.assertTrue("people_in" in linegraph)
        self.assertTrue("people_out" in linegraph)
        labels = linegraph.get("label")
        people_in = linegraph.get("people_in")
        people_out = linegraph.get("people_out")
        self.assertTrue(isinstance(labels, list))
        self.assertTrue(isinstance(people_in, list))
        self.assertTrue(isinstance(people_out, list))
        self.assertTrue(len(labels) == len(people_in))
        self.assertTrue(len(labels) == len(people_out))
