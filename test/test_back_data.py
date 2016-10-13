from backup_sql import BackupData
from nose.tools import with_setup
import json
import collections

DICT ={'table': 'compositions', 'values': {'1': {'component_id': '2', 'product_id': '1', 'line_num': 'NULL', 'created_at': 'NULL', 'updated_at': 'NULL', 'fixed': 'NULL', 'quantity': '1.000'}, '3': {'component_id': '190', 'product_id': 'NULL', 'line_num': 'NULL', 'created_at': '2008-07-24 10:27:34', 'updated_at': '2008-07-24 10:27:34', 'fixed': 'NULL', 'quantity': '5.000'}, '2': {'component_id': '3', 'product_id': '1', 'line_num': 'NULL', 'created_at': 'NULL', 'updated_at': 'NULL', 'fixed': 'NULL', 'quantity': '1.000'}, '4': {'component_id': '358', 'product_id': '259', 'line_num': '80', 'created_at': '2008-11-19 16:50:36', 'updated_at': '2008-11-19 16:52:20', 'fixed': '1', 'quantity': '1.000'}}, 'primary_key': 'id', 'fields': {'component_id': ['int(11)', 'default NULL'], 'product_id': ['int(11)', 'default NULL'], 'line_num': ['int(11)', 'default NULL'], 'created_at': ['datetime', 'default NULL'], 'updated_at': ['datetime', 'default NULL'], 'fixed': ['tinyint(1)', 'default NULL'], 'id': ['int(11)', 'NOT NULL auto_irement'], 'quantity': ['decimal(15,3)', "default '1.000'"]}}

JSON1 = """{"table": "compositions", "values": {"1": {"component_id": "2", "product_id": "1", "line_num": "NULL", "created_at": "NULL", "updated_at": "NULL", "fixed": "NULL", "quantity": "1.000"}, "3": {"component_id": "190", "product_id": "NULL", "line_num": "NULL", "created_at": "2008-07-24 10:27:34", "updated_at": "2008-07-24 10:27:34", "fixed": "NULL", "quantity": "5.000"}, "2": {"component_id": "3", "product_id": "1", "line_num": "NULL", "created_at": "NULL", "updated_at": "NULL", "fixed": "NULL", "quantity": "1.000"}, "4": {"component_id": "358", "product_id": "259", "line_num": "80", "created_at": "2008-11-19 16:50:36", "updated_at": "2008-11-19 16:52:20", "fixed": "1", "quantity": "1.000"}}, "primary_key": "id", "fields": {"component_id": ["int(11)", "default NULL"], "product_id": ["int(11)", "default NULL"], "line_num": ["int(11)", "default NULL"], "created_at": ["datetime", "default NULL"], "fixed": ["tinyint(1)", "default NULL"], "updated_at": ["datetime", "default NULL"], "quantity": ["decimal(15,3)", "default '1.000'"], "id": ["int(11)", "NOT NULL auto_irement"]}}"""

JSON2 = """{"table": "compositions", "values": {"3": {"component_id": "190", "product_id": "NULL", "line_num": "NULL", "created_at": "2008-07-24 10:27:34", "updated_at": "2008-07-25 10:27:34", "fixed": "NULL", "quantity": "5.000"}, "4": {"component_id": "358", "product_id": "259", "line_num": "80", "created_at": "2008-11-18 16:50:36", "updated_at": "2008-11-18 16:52:20", "fixed": "1", "quantity": "1.000"}}, "primary_key": "id", "fields": {"component_id": ["int(11)", "default NULL"], "product_id": ["int(11)", "default NULL"], "line_num": ["int(11)", "default NULL"], "created_at": ["datetime", "default NULL"], "fixed": ["tinyint(1)", "default NULL"], "updated_at": ["datetime", "default NULL"], "quantity": ["decimal(15,3)", "default '1.000'"], "id": ["int(11)", "NOT NULL auto_irement"]}}"""

def test_loading_from_dictionay():
  test_data = BackupData()
  test_data.load_from_dict(DICT)
  assert test_data.content == DICT
  assert test_data.json == JSON1

def test_loading_from_json():
  test_data = BackupData()
  test_data.load_from_json(JSON1)
  assert test_data.content == DICT
  assert test_data.json == JSON1

def test_combining_json():
  obj_1 = BackupData()
  obj_1.load_from_json(JSON1)
  obj_2 = obj_1.combine_json(JSON2)
  
  # Newer value updates
  assert obj_2.content["values"]["3"]["updated_at"] == "2008-07-25 10:27:34"
  # Older value in json2 is not used
  assert obj_2.content["values"]["4"]["updated_at"] == "2008-11-19 16:52:20"
  
def test_generating_unique_name():
  obj = BackupData()
  obj.load_from_json(JSON1)
  assert obj.name == "compositions_4_2008-11-19_16-52-20"
