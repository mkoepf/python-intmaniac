CHANGELOG
=========

0.9.1 - 0.9.3
-------------

Date: 2016-03-02

- Fixed console invocation bug in three attempts
- Fixed bug in main execution loop
- Added test for main execution loop


0.9.0
-----

- Removed multi-threaded execution of tests / test sets
- Changed file format (moved ``test_commands`` out of ``meta`` subdict)
- Changed file format (no more "arrays of test sets")
- Changed execution order of tests (in alphabetical order by test set key), same for tests
- Added explicit test for ``test_commands``, ``meta.test_before``, ``meta.test_after`` command construction


0.8.0
-----

- TeamCity outputs pretty sensbile now


0.7.0
-----

- added configuration fields ``test_before`` and ``test_after``
- won't mention "cleanup and bugfixes" any more


0.6.0
-----

- changed test directory logic, is now ``$pwd/intmaniac_$PID`` by default
- command line settings override everything now
- fixed a couple of bugs
- internal restructuring


0.5.2
-----

- fixed bug in cleanup command execution
- fixed bug in exception logging (yeah)
- fixed logging output diarrhoe


0.5.1
-----

- fixed string handling bug


0.5.0
-----

- Switched to ``popen()`` for command execution because of thread-safety (setting of current working directory)
- Create a log file with all output by default now in ``base_dir``
- Fixed a couple of python 3 string / bytes handling issues
- Internal refactoring and restructuring


0.4.1
-----

- Documentation update (added CHANGES.rst, README.rst for pypi)
- Unit testing available in python 2.x now with external mock module
- Internal changes
