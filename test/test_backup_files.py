import os
import unittest
from backup_sql import ParsedData
import backup_sql
import collections

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
BACKUP_DIR = os.path.join(CUR_DIR, "backup_files")
BACKUP_FILE_MDP = """--
-- Definition of table `compositions`
--

DROP TABLE IF EXISTS `compositions`;
CREATE TABLE `compositions` (
 `id` int(11) NOT NULL auto_increment,
 `product_id` int(11) default NULL,
 `component_id` int(11) default NULL,
 `created_at` datetime default NULL,
 `updated_at` datetime default NULL,
 `quantity` decimal(15,3) default '1.000',
 `line_num` int(11) default NULL,
 `fixed` tinyint(1) default NULL,
 PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `compositions`
--

/*!40000 ALTER TABLE `compositions` DISABLE KEYS */;
INSERT INTO `compositions`
(`id`,`product_id`,`component_id`,`created_at`,`updated_at`,`quantity`,`line_num`,`fixed`)
VALUES
 (1,1,2,NULL,NULL,'1.000',NULL,NULL),
 (2,1,3,NULL,NULL,'1.000',NULL,NULL),
 (3,NULL,190,'2008-07-24 10:27:34','2008-07-24 10:27:34','5.000',NULL,NULL),
 (4,259,358,'2008-11-19 16:50:36','2008-11-19 16:52:20','1.000',80,1);
"""

class TestParsingBackupFile(unittest.TestCase):
  def setUp(self):
    self.mdp_parsed = ParsedData(BACKUP_FILE_MDP)
    self.actual_fields = collections.OrderedDict([
                   ('id', ['int(11)', 'NOT NULL auto_increment']),
                   ('product_id', ['int(11)', 'default NULL']),
                   ('component_id', ['int(11)', 'default NULL']),
                   ('created_at', ['datetime', 'default NULL']),
                   ('updated_at', ['datetime', 'default NULL']),
                   ('quantity', ['decimal(15,3)', "default '1.000'"]),
                   ('line_num', ['int(11)', 'default NULL']),
                   ('fixed', ['tinyint(1)', 'default NULL'])])
    self.actual_values={
                  '1': {'product_id':'1', 'component_id':'2', 'created_at':'NULL', 'updated_at':'NULL','quantity':'1.000', 'line_num':'NULL', 'fixed': 'NULL'},
                  '2': {'product_id':'1', 'component_id':'3', 'created_at':'NULL', 'updated_at':'NULL','quantity':'1.000', 'line_num':'NULL', 'fixed': 'NULL'},
                  '3': {'product_id':'NULL', 'component_id':'190', 'created_at':'2008-07-24 10:27:34', 'updated_at':'2008-07-24 10:27:34','quantity':'5.000', 'line_num':'NULL', 'fixed': 'NULL'},
                  '4': {'product_id':'259', 'component_id':'358', 'created_at':'2008-11-19 16:50:36', 'updated_at':'2008-11-19 16:52:20','quantity':'1.000', 'line_num':'80', 'fixed': '1'}}

    self.actual_full_object = {'table': "compositions",
                               'fields': dict(self.actual_fields),
                               'values': self.actual_values,
                               'primary_key': 'id'}

  def test_getting_all_files_in_abs_dir(self):
    full_path_dir = os.path.abspath(BACKUP_DIR)
    calc_files = backup_sql.get_all_file_names(full_path_dir)
    def_files = map(lambda x: os.path.join(full_path_dir, x), ["backup_file_mdp.txt", "backup_file_xrf.txt"])
    assert calc_files == def_files
    
  def test_reading_backup_file(self):
    file_path = os.path.join(BACKUP_DIR, "backup_file_mdp.txt")
    file_string = backup_sql.read_file(file_path)
    assert  file_string == BACKUP_FILE_MDP

  def test_get_table_name(self):
    assert self.mdp_parsed.table == "compositions"

  def test_get_fields(self):
    assert self.mdp_parsed.fields == self.actual_fields

  def test_get_primary_key(self):
    assert self.mdp_parsed.primary_key == 'id'

  def test_get_values(self):
    assert self.mdp_parsed.values == self.actual_values

  def test_parsing_backup_file_into_python_object(self):
    assert self.mdp_parsed.generate_full_object() == self.actual_full_object
