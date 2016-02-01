CHANGELOG
=========

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
