# Logging



1. Log levels
2. Service configuration
3. Log file integration



## 1. Log levels

We try to provide a common logging setup for all roles. All roles that can be
tuned in verbosity are expected to have a '{{rolename}}_log_level' setting to
adjust that verbosity. All possible values for this setting are
* `none`: As little logging as possible
* `error`: Only log errors and worse
* `info`: Log informational messages and worse
* `debug`: Log general debug messages and worse
* `all`: Log every possible detail
Using only these five values makes it easy for users to adjust verbosity of
services without having to learn configuration details of the services, while
still being able to cover many use cases.



## 2. Service configuration

Of course, the services typically do not use the above 5 level, but have their
own levels. It's the role's responsibility to map between the values. There are
some filters that lessen this burden.  There is for example the general purpose
`logging_map_level`. And for some standard environments there are preconfigured filters, like `logging_map_level_python`, `logging_map_level_java_jul`, or `logging_map_level_java_log4j`.

`logging_map_level` takes 6 parameters. The first is the set log level. The
other parameters are the expected outcomes from least to most verbose. So for
example using

```
LogLevel {{apache_webserver_log_level | logging_map_level('emerg', 'error', 'info', 'trace2', 'trace8')}}
```

becomes `LogLevel emerg`, if `apache_webserver_log_level` is `none`, and
`LogLevel trace8`, if `apache_webserver_log_level` is `all`.

`logging_map_level_{environment}` helps to translate log levels for standard
environments. For example:

```
com.mycompany.component = {{app_log_level | logging_map_level_java_jul}}
```

becomes `com.mycompany.component = SEVERE` if `app_log_level` is `error`, and
`com.mycompany.component = FINE` if `app_log_level` is `debug`.



## 3. Log file integration

To allow the environment to integrate log files (e.g.: Automatically generate a
row for it on the host's dashboard), we collect them in the global
`logging_log_files` list. Each item in that list specifies a log file and is
either a string (which is an abbreviation for `{'file': '<string>'}`) or
directly a dictionary This dictionary can have the following key/values:
* `file`: The absolute path to the log file.
* `format`: (Default: `custom`) The format of the logs in the file. It has to be
  one of the following:
  * `custom`: Undefined format. Only basic line counts are evaluated
  * `python`: Python log output formatted by `logging_default_format_python`,
    and `logging_default_format_python_date`
* `description: (Default: `Custom log file at ` + file) A description for the
  file for humans.
* `group`: (Default: `ungrouped`) A group for the file. This group is optional,
  but may be used for structure. For example the file's metrics are filed
  underneath the group.
* `item`: (Default: file name with all of `.`, `_`, and `/` replaced by `_`) A
  description of the item for machines. This is typically used as 2nd level
  grouping. Items should be unique for a given group.
* `skip: (Default: False) If true, skip this log file. This is useful simplify
  config and get it more static, while still allowing to only use relevant
  files. E.g.: If the log level is none, some file might not get written and can
  get ignored by setting `skip` to True.
* `slug: (Default: group `-` item) id to be used for sorting.
