CMFOpenFlow
###########

Copyright 2002 of RefLab (www.reflab.it)
Ciriaci Francesco
Vincenzo Di Somma
Riccardo Lemmi


CMFOpenFlow is based on the Icube product OpenFlow,
Copyright 2002 Icube (www.icube.it www.openflow.it)

Overview
********

Problem:
========

The design and development of workflow applications can be often divided into
two different parts. The first part, Workflow Systems Management, concerns the
creation of a custom framework, data structures and metadata to manage the
distribution of tasks and to store the information collected during each task.
The second part, Workflow Applications Management, is associated with creating
the user applications and providing workflow-oriented hooks to assist those
applications in managing workflow instances, objects and reports.

Goals of CMFOpenFlow :
======================

Provide tools which simplify Workflow Systems Management activities by providing
a workflow engine that will be able to build the Process Definition Map, handle
the Process Definition Instance, and help to provide worklist interaction hooks
and reports, as well as realtime Process Instance history and statistical
reports.

 - Provide general-purpose support for Workflow exception handling

 - Provide support for easily modifying the Process Definitions to adapt the
   workflow as needed, using statistical and exception-tracking reports as well as
   changing workflow conditions.

 - Provide support for simplifying Workflow Applications Management by providing
   hooks and methodologies for creating and managing workflow-generated objects and
   data.

 - Provide integration for CMF/Plone site.

Requirements
************

Tested with Zope 2.5.1 and 2.6.1

License
*******

CMFOpenflow is released under the General Public Licence (GPL).

Installation
************

Unpack the .tgz and put the CMFOpenflow directory in ...lib/python/Products
Restart Zope

Standalone
==========

Add a 'Openflow (Reflab)' object to your folder.

Tool
====

To instantiate portal_openflow in your CMF/Plone portal, create an external
method with:

   - Id : Install_CMFOpenflow

   - Module Name : CMFOpenflow.Install

   - Function Name : install

and test it.

Home page and documentation
***************************

http://www.reflab.it/community

Bug reports
***********

Bug reports may be sent to riccado@reflab.it

Mailing list
************

collective-cmfopenflow-request@lists.sourceforge.net

