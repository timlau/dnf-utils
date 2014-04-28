##############################
 dnf-utils Command Reference
##############################

Description
===========

`dnf-utils` is collection of add-on tool for dnf

Available commands are:

* query
* dnl

See the reference for each command below.

Query Command
==============

Query packages and list result in user defined format

Synopsis
--------

``dnf query [cmd-options] [<key>]``

Arguments
----------

``<key>``
    the key to search for in package names.    

Cmd Options
------------

``--show-help``
    show this help about this tool
    
``--all``         
    query in all packages (Default)
    
``--installed``
    query in installed packages
    
``--latest``           
    show only latest packages
    
``--qf QUERYFORMAT, --queryformat QUERYFORMAT``
    format for displaying found packages
    
``--repoid REPO``
    show only results from this REPO
    
``--arch ARCH``         
    show only results from this ARCH
    
``--whatprovides REQ``
    show only results there provides REQ
    
``--whatrequires REQ``    
    show only results there requires REQ
    
``-showtags``   
    show available tags to use with --queryformat




Examples
--------
``dnf query kernel --installed --qf "%{name}"``
    list names of installed packages with **kernel** in the name
    
``dnf query --installed --arch i686``
    show all installed packages with the **i686** archictecture
    
``dnf query --installed --whatrequires "dnf"``
    show installed packages there is requiring **dnf**


