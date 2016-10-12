from sql_backup_data import SQLBackup
import sqlite3

def setup_sqlite():
  "generate sqlite db with some data"

def teardown_sqlite():
  "teardown to make test idempotent"
 
@with_setup(setup_sqlite, teardown_sqlite)
def test_inserting_new_json_object_into_sqlite()
  pass

@with_setup(setup_sqlite, teardown_sqlite)
def test_inserting_most_recent_json_object_into_sqlite()
  pass

@with_setup(setup_sqlite, teardown_sqlite)
def test_inserting_out_of_date_existing_json_object_into_sqlite()
  pass

def test_loading_json_object_into_postgres()
  pass
