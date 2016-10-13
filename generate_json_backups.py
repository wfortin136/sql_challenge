import backup_sql
from backup_sql import ParsedData
from backup_sql import BackupData
import argparse
import json
import os

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='A script to generate json files of all db backup files in a directory')
  parser.add_argument('-d','--dir', help='Input Absolute Path to Directory',required=True)
  args = parser.parse_args() 

  # Parse Files
  files = backup_sql.get_all_file_names(args.dir)
  parsed_data = []
  for file in files:
    parsed_data.append(ParsedData(backup_sql.read_file(file)))
  
  # Store for manipulation
  backup_data = []
  for parsed in parsed_data:
    data = BackupData()
    data.load_from_dict(parsed.generate_full_object())
    backup_data.append(data)

  # Save each file as json file
  json_dir = os.path.join(args.dir, 'json')
  if not os.path.exists(json_dir):
    os.makedirs(json_dir)

  for backup in backup_data:
    json_file = os.path.join(json_dir, backup.name)
    with open(json_file+'.json', 'w') as output_file:
      json.dump(backup.json, output_file)

  # Generate single up-to-date object
  latest_snapshot = backup_data[0]
  for backup in backup_data[1:]:
    latest_snapshot = backup.combine_dict(latest_snapshot.content)

  json_file = os.path.join(args.dir, 'json', latest_snapshot.get_table_name())
  with open(json_file+'.json', 'w') as output_file:
    json.dump(latest_snapshot.json, output_file)
  
