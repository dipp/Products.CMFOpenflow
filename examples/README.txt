IssuesTracking_App.xml

    It containts the core application of issues tracking system.
    It Requires 'process_openflow' and the process model.

IssuesTracking_Model.xml

    This is the process's model of issues tracking system.
    You can import this in the portal_openflow (or whatever
    CMFOpenflow object)

CMFOpenflowTest.xml

    This is the export of a CMF portal that contains the previous
    application and model.

The system has 4 user: customer, supervisor, supporterhw, supportersw.

The user's roles are:
customer: Member, Customer
supervisor: Member, Supervisor
supporterhw: Member, SupporterHW
supportersw: Member, SupporterSW

Requirements:
 CMF 1.3
 CMFOpenflow

If your installation is not a Debian, you should change the link for
the skins to the CMF file system folders.

For CMFOpenflowTest it's recommended to make an 'update Catalog' of
the 'portal_catalog'.


