.. py:currentmodule:: lsst.daf.butler

.. _lsst.daf.butler:

###############
lsst.daf.butler
###############

This module provides an abstracted data access interface, known as the Butler.
It can be used to read and write data without having to know the details of file formats or locations.

.. _lsst.daf.butler-contributing:

Contributing
============

``lsst.daf.butler`` is developed at https://github.com/lsst/daf_butler.
You can find Jira issues for this module under the `daf_butler <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20component%20%3D%20daf_butler>`_ component.

.. _lsst.daf.butler-pyapi:

Python API reference
====================

.. automodapi:: lsst.daf.butler
   :no-main-docstr:

Example datastores
------------------

.. automodapi:: lsst.daf.butler.datastores.posixDatastore
   :no-main-docstr:
   :headings: ^"
.. automodapi:: lsst.daf.butler.datastores.inMemoryDatastore
   :no-main-docstr:
   :headings: ^"
.. automodapi:: lsst.daf.butler.datastores.chainedDatastore
   :no-main-docstr:
   :headings: ^"

Example registries
------------------

.. automodapi:: lsst.daf.butler.registries.sqlRegistry
   :no-main-docstr:
   :headings: ^"

Example formatters
------------------

.. automodapi:: lsst.daf.butler.formatters.fileFormatter
   :no-main-docstr:
   :headings: ^"
.. automodapi:: lsst.daf.butler.formatters.jsonFormatter
   :no-main-docstr:
   :headings: ^"
.. automodapi:: lsst.daf.butler.formatters.yamlFormatter
   :no-main-docstr:
   :headings: ^"
.. automodapi:: lsst.daf.butler.formatters.pickleFormatter
   :no-main-docstr:
   :headings: ^"

Support API
-----------

.. automodapi:: lsst.daf.butler.core.safeFileIo
   :no-main-docstr:
   :headings: ^"
.. automodapi:: lsst.daf.butler.core.utils
   :no-main-docstr:
   :headings: ^"
.. automodapi:: lsst.daf.butler.core.repoRelocation
   :no-main-docstr:
   :headings: ^"
   :include-all-objects:
