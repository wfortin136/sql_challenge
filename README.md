# Code Challenge 199: Restoring Data From SQL

## Summary
From http://rubyquiz.strd6.com/quizzes/199-restoring-data-from-sql


I chose to restore sql data from a series of backup files for a specified table.
However, while there were some interesting aspects, the basic problem and solution 
were a bit trivial. So I decided to slightly reframe the problem.


If you had a set of db backup files, you want to be able to store that data
as key value pairs in a nosql db for time series anlysis, reconstituting data to a specific 
snapshot in time,  or have the ability to migrate your data to another db (i.e. snapshots of mysql -> postgres). 
While this challenge won't solve the problem in it's entirety, it builds the 
foundation for such an environment. Specifically, the code will:
* Read and parse a set of backup files from a directory
* It will store that information in a python object that will provide reversible transformation
between a python object and json blob
* It will allow multiple backup json blobs to be combined into a single json blob

Additional assumptions I'm making to make the problem more interesting:
* Table Schema may have changed over time (Alter or deletion of a column)
* The code must be able to support any table and schema
* We want to persist the storage of the intermediate data sets. That is, store each backup file

## Approach
* Open each file within a directory in any order.
  * Assume we cannot use timestamp of files for ordering
  * Assume name has no timestamp indicator (Though it probably should)
* Store each file as a python object into memory
* Convert each python object to a json blob
* Be able to read each json and convert back into python object
* Be able to collate multiple json objects into a single json object reflecting latest state of data

## Requirements
* python 2.7
* pip

## Setup Instructions
We will first use virtualenv to isolate our python environment and the specific
dependencies and packages for this project
```sh
$ cd <root_dorectory_of_this_repo>
$ virtualenv .
$ source bin/activate
```
We are now inside our virtual environment specific to this project.
We will now install the dependencies for this project
```sh
$ pip install -r requirements.txt
```

## Run
```sh
$ python generate_json_backups.py -d /abs_path_to/test/backup_files
$ python generate_json_backups.py -h 
```
You should be able to check the test/backup_files/json/ directory and see each backup file
as well as the combination of those files, taking precedence on latest data

## Tests
```sh
$ nosetests -s -v
```
