
DNF Utils
==========

This project contains community add-on tools for DNF

The tools is **not maintained** by the DNF team, but by the individual tools authors.

The tools are dnf plugins there is extending dnf with extra commands.

the tools are executed by running

```
dnf <commmand> [parameters]
```

to get help about the tool, use the following command

```
dnf <command> --help-<command>
```

Example: (To get help about the **query** tool)

```
dnf query --help-query
```

Tools
======

* **query** is simplified version of repoquery from yum-utils


Contribution:
==============

If you want to make a new tool.

1. Make a fork of this project
2. Use the plugins/sample.py as a template of an new util and make it your own (See the TODO's in the code)
3. Follow the [DNF hacking guidelines](https://github.com/akozumpl/dnf/wiki/Hacking)
4. Code must work in both Python 2 & 3, if possible
5. The tool must contain a --help-<command> there is displaying help about the tool
6. If it make sense, then add unittest for testing your code
6. Submit a pull request for your new tool


Other Projects:
================
* [DNF](https://github.com/akozumpl/dnf)
* [dnf-plugins-core](https://github.com/akozumpl/dnf-plugins-core) plugins maintained by the DNF team











