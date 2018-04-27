RobotFramework Elasticsearch Library
========================================

|Build Status|

Short Description
-----------------

`Robot Framework`_ library for working with Elasticsearch using `Elasticsearch`_ python library.

Installation
------------

::

    pip install robotframework-elasticsearchlibrary

Documentation
-------------

See keyword documentation for ElasticsearchLibrary in folder ``docs``.

Example
-------
+-----------+----------------------+
| Settings  |         Value        |
+===========+======================+
|  Library  | ElasticsearchLibrary |
+-----------+----------------------+

+---------------+-------------------------------------+-----------------+---------------+----------------+
|  Test cases   |               Action                |     Argument    |    Argument   |    Argument    |
+===============+=====================================+=================+===============+================+
|  Simple Test  | Connect To Elasticsearch            | 192.168.1.108   | 9200          | alias=cluster1 |
+---------------+-------------------------------------+-----------------+---------------+----------------+
|               | Es Save Data                        | some_string1    |               |                |
+---------------+-------------------------------------+-----------------+---------------+----------------+
|               | ${search_result}=                   | Es Search       | some_string2  |                |
+---------------+-------------------------------------+-----------------+---------------+----------------+
|               | Close All Elasticsearch Connections |                 |               |                |
+---------------+-------------------------------------+-----------------+---------------+----------------+

License
-------

Apache License 2.0

.. _Robot Framework: http://www.robotframework.org
.. _Elasticsearch: https://pypi.org/project/elasticsearch/

.. |Build Status| image:: https://travis-ci.org/peterservice-rnd/robotframework-elasticsearchlibrary.svg?branch=master
   :target: https://travis-ci.org/peterservice-rnd/robotframework-elasticsearchlibrary