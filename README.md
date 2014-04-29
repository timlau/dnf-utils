
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
dnf <command> --show-help
```

Tools
======

* **query** is simplified version of repoquery from yum-utils
* **dnl** is simplified version of yumdownloader from yum-utils

Install:
==========

Run this as root from the git checkout to install the tool

```
make install
```

or install the latest test build from the (COPR Repository)[http://copr-fe.cloud.fedoraproject.org/coprs/timlau/dnf-utils/]



Documentation:
===============
[Online Documentation](http://dnf-utils.readthedocs.org/en/latest/index.html)


Contribution:
==============

If you want to make a new tool.

1. Make a fork of this project
2. Use the plugins/sample.py as a template of an new util and make it your own (See the TODO's in the code)
3. Follow the [DNF hacking guidelines](https://github.com/akozumpl/dnf/wiki/Hacking)
4. Code must work in both Python 2 & 3, if possible
5. If it make sense, then add unittest for testing your code
6. Submit a pull request for your new tool


Other Projects:
================
* [DNF](https://github.com/akozumpl/dnf)
* [dnf-plugins-core](https://github.com/akozumpl/dnf-plugins-core) plugins maintained by the DNF team











