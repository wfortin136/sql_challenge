import os
import re
import collections
import shlex
import json

def get_all_file_names(directory):
  """directory must be absolute path. 
  Returns an array with the fully qualified name"""
  return map(lambda x:os.path.join(directory, x) , os.listdir(directory))

def read_file(file):
  """file is a string of the absolute path to the file.
  Returns a string representation of the file"""
  with open(file, 'r') as f:
    file_string = f.read()
  return file_string

class ParsedData(object):
  
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

  def __init__(self):
    self.content = {}
    self.json = ''

  def load_from_dict(self, dictionary):
    self.content = dictionary
    self.__update_json()

  def load_from_json(self, json):
    self.json = json
    self.__update_content()

  def __update_json(self):
    self.json = json.dumps(self.content)

  def __update_content(self):
    self.content = json.loads(self.json)
  
  def combine_json(self, json2):
    dict2 = json.loads(json2)
    return self.combine_dict(dict2)

  def combine_dict(self, dict2):
    
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
      if key in large_set:
        updated_l = large_set[key]["updated_at"]
        updated_s = small_set[key]["updated_at"]
        if updated_l == 'NULL':
          if updated_s != 'NULL':
            subset[key] = small_set[key]
        else:
          if updated_s == 'NULL':
            subset[key] = large_set[key]
          else:
            if updated_l > updated_s:
              subset[key] = large_set[key]
            else:
              subset[key] =small_set[key]
    base_set["values"].update(subset)
    new_obj = BackupData()
    new_obj.load_from_dict(base_set)
    return new_obj 
