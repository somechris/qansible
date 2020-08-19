Role: common-directories
========================



1. Description
2. Globals
3. Parameters



1. Description
--------------

Sets up commonly use directories on a host.



2. Globals
----------

* `common_directories_db`: This directories holds database files for
  services.
* `common_directories_data_base`: Base directory for data
  directories. Data directories should hold all files/directories that
  might eventually be too big to fit on a small root partition.
* `common_directories_data_dir1`: First data directory.
* `common_directories_data_dir2`: Second data directory.
* `common_directories_default_data_dir`: (Default: value of
  `common_directories_data_dir2`) Default data directory to use.



3. Parameters
-------------

This role does not have parameters.
