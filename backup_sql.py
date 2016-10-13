import os
import re
import collections
import shlex
import json

def get_all_file_names(directory):
  """directory must be absolute path. 
  Returns an array with the fully qualified name"""
  files = map(lambda x:os.path.join(directory, x), os.listdir(directory))
  return [f for f in files if os.path.isfile(f)]

def read_file(file):
  """file is a string of the absolute path to the file.
  Returns a string representation of the file"""
  with open(file, 'r') as f:
    file_string = f.read()
  return file_string

class ParsedData(object):
  """Parse and store backup data from a backup file
  """
  def __init__(self, file_str):
    self.table = self.__get_table_name(file_str)
    self.fields = self.__get_fields(file_str)
    self.primary_key = self.fields.keys()[0]
    self.values = self.__get_values(file_str)
  
  def __get_table_name(self, data_str):
    match_obj = re.search(r'-- Definition of table `(.*)`' , data_str)
    return match_obj.group(1)

  def __get_fields(self, data_str):
    begin = data_str.find("CREATE TABLE")
    end = data_str.find("ENGINE")
    fields = collections.OrderedDict()

    #Get the segment that defines the tables and parse each line
    for line in data_str[begin:end].splitlines():
      exp = re.search(' `(.*?)` (.*?)\s(.+?)(\,)?$', line)
      if exp:
        fields[exp.group(1)] = [exp.group(2), exp.group(3)]
    return fields

  def __get_values(self, data_str):
    begin = data_str.find("VALUES")
    values = {}
    for line in data_str[begin:].splitlines():
      exp = re.search(' \((.*?),(.*)\)', line)
      if exp:
        key = exp.group(1)
        field_vals = shlex.split(exp.group(2))[0].split(',')
        field_vals_dict = {}
        for ordered_key in self.fields.keys()[1:]:
          field_vals_dict[ordered_key] = field_vals.pop(0)
        values[key] = field_vals_dict
    return values

  def generate_full_object(self):
    return {'table': self.table,
            'fields': dict(self.fields),
            'values': self.values,
            'primary_key': self.primary_key}

class BackupData(object):
  """Load backup data from either json or dict and store as python obj for analysis
  """
  def __init__(self):
    self.content = {}
    self.json = ''
    self.name = ''

  def load_from_dict(self, dictionary):
    self.content = dictionary
    self.__update_json()
    self.__set_name()

  def load_from_json(self, json):
    self.json = json
    self.__update_content()
    self.__set_name()

  def __update_json(self):
    self.json = json.dumps(self.content)

  def __update_content(self):
    self.content = json.loads(self.json)
  
  def combine_json(self, json2):
    """Will return a new BackupData object with updated set
       keep self and passed objecy immutable
    """
    dict2 = json.loads(json2)
    return self.combine_dict(dict2)
  
  def __set_name(self):
    """name will include table name and latest timestamp in file
    """
    table_name = self.get_table_name()
    record, timestamp = self.__get_max_timestamp()
    self.name = "%s_%s_%s" % (table_name, record, timestamp)

  def get_table_name(self):
    return self.content["table"]

  def __get_max_timestamp(self):
    max_timestamp = ''
    index = '0'
    for key, value in self.content["values"].iteritems():
      cur_timestamp = value["updated_at"]
      if cur_timestamp != 'NULL':
        if max_timestamp == '' or cur_timestamp > max_timestamp:
          max_timestamp = cur_timestamp
          index = key

    return index, max_timestamp.replace(' ', '_').replace(':','-')

  def combine_dict(self, dict2):
    """Will return a new BackupData object with updated set
       keep self and passed objecy immutable
    """
    # iterate through smaller data set
    # base_set will be the larger set and is used for updating
    if len(self.content["values"]) > len(dict2["values"]):
      large_set = self.content["values"]
      small_set = dict2["values"]
      base_set = self.content
    else:
      small_set = self.content["values"]
      large_set = dict2["values"]
      base_set = dict2

    subset = {}
    for key in small_set.keys():
      # determine wether to compare keys
      if key in large_set:
        updated_l = large_set[key]["updated_at"]
        updated_s = small_set[key]["updated_at"]
        if updated_l == 'NULL':
          if updated_s != 'NULL':
            # update to not NULL set
            # if both updated_at are NULL, things
            # are ambiguos. We could defer to created_at
            # but for simplicity we will default to
            # the values in the larger set
            subset[key] = small_set[key]
        else:
          if updated_s == 'NULL':
            # update to not NULL set
            subset[key] = large_set[key]
          else:
            if updated_l > updated_s:
              subset[key] = large_set[key]
            else:
              subset[key] =small_set[key]
      else:
        subset[key] = small_set[key]
    base_set["values"].update(subset)
    new_obj = BackupData()
    new_obj.load_from_dict(base_set)
    return new_obj 
