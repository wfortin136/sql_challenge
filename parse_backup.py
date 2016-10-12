import os
import re

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

def parse_string(data_str):
  """backup_data is a string of the full data set
  Returns a python dictionary"""
  table = get_table_name(data_str)

def get_table_name(data_str):
  match_obj = re.search(r'-- Definition of table `(.*)`' , data_str)
  return match_obj.group(1)

def get_fields(data_str):
  begin = data_str.find("CREATE TABLE")
  end = data_str.find("ENGINE")
  fields = {}
  for line in data_str[begin:end].splitlines():
    exp = re.search(r' `(.*)` (.*?)\s(.*)', line)
    if exp:
      fields[exp.group(1)] = [exp.group(2), exp.group(3)]
  return fields
