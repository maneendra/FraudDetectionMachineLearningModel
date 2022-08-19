'''
Created on 1 Feb 2022

@author: Maneendra Perera
'''
import unittest
from src.data.bigquery import create_bigquery_connection

class BigQueryTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.project_id = 'ultra-palisade-339421';

    def test_create_bigquery_connection(self):
        self.assertTrue(create_bigquery_connection(self.project_id), "BigQuery Connection is Success.");