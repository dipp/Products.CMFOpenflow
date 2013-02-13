from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware
from DateTime import DateTime
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from zLOG import LOG, ERROR, INFO


class activity(CatalogPathAware, SimpleItem):
    """ Each activity is responsible for doing something and then forwarding
    the instance """

    def __init__(self,
                 id,
                 process_id,
                 split_mode='and',
                 join_mode='and',
                 auto_push_mode=0,
                 start_mode=0,
                 finish_mode=1,
                 subflow='',
                 push_application='',
                 application='',
                 parameters='{}',
                 title='',
                 description='',
                 kind='dummy',
                 limit=0):
        self.id = id
        self.process_id = process_id
        self.split_mode = split_mode        # 'and', 'xor'
        self.join_mode = join_mode          # 'and', 'xor'
        self.auto_push_mode = auto_push_mode
        self.start_mode = start_mode
        self.finish_mode = finish_mode
        self.subflow = subflow
        self.kind = kind
        # kind may be dummy, standard or subflow
        self.application = application
        self.push_application = push_application
        self.title = title
        self.parameters = parameters
        self.description = description
        self.limit = limit
        # permission
        self._push_roles = ['Manager',]
        self._pull_roles = ['Manager',]


    manage_options = ({'label': 'Edit', 'action': 'index_html'},
                      {'label': 'Permissions', 'action': 'permissionsForm'},)

    security = ClassSecurityInfo()


    security.declareProtected('Use OpenFlow', 'index_html')
    index_html = PageTemplateFile('zpt/activity/manage_editActivityForm', globals())

    security.declareProtected('Manage OpenFlow', 'permissionsForm')
    permissionsForm = PageTemplateFile('zpt/activity/manage_permissionsActivityForm', globals())


    meta_type = 'Activity'


    security.declareProtected('Manage OpenFlow', 'edit')
    def edit(self,
             split_mode=None,
             join_mode=None,
             start_mode=None,
             finish_mode=None,
             push_application=None,
             auto_push_mode=None,
             application=None,
             title=None,
             description=None,
             limit=None,
             kind=None,
             subflow=None,
             REQUEST=None):


        """ changes the activity settings """
        # mode refers to the kind of routing the instance has to undergo
        # and it is either 'and' or 'xor'
        if split_mode:
            self.split_mode = split_mode
        if join_mode:
            self.join_mode = join_mode

        if start_mode:
            self.start_mode = 1
        else:
            self.start_mode = 0

        if finish_mode:
            self.finish_mode = 1
        else:
            self.finish_mode = 0

        if kind:
            self.kind = kind
        if application and self.kind=='standard':
            self.application = application
        elif self.kind!='standard':
            self.application = None
        if push_application:
            self.push_application = push_application
        if auto_push_mode:
            self.auto_push_mode = 1
        else:
            self.auto_push_mode = 0
            self.push_application = None

        if title:
            self.title = title
        if description:
            self.description = description
        if limit:
            self.limit = limit

        if subflow and self.kind=='subflow':
            self.subflow = subflow
        elif self.kind!='subflow':
            self.subflow = None

        self.reindex_object()

        if REQUEST: REQUEST.RESPONSE.redirect('..')


    security.declareProtected('Manage OpenFlow', 'title_or_id')
    def title_or_id(self):
      """ """
      if self.title:
        return self.title
      else:
        return self.id


    def getIncomingTransitionsNumber(self):
        """ returns all the process transition objects that go to the specified activity """
        return len(filter(lambda x, activity_id=self.id : x.To==activity_id, self.aq_parent.objectValues('Transition')))


    security.declareProtected('Manage OpenFlow', 'isAutoStart')
    def isAutoStart(self):
        """ returns true if the activity start mode is automatic"""
        return self.start_mode and self.kind == 'standard'


    security.declareProtected('Manage OpenFlow', 'isAutoFinish')
    def isAutoFinish(self):
        """ returns true if the activity finish mode is automatic"""
        return self.finish_mode == 1


    security.declareProtected('Manage OpenFlow', 'isStandard')
    def isStandard(self):
        """ returns true if the activity is of 'standard' kind """
        return self.kind == 'standard'


    security.declareProtected('Manage OpenFlow', 'isSubflow')
    def isSubflow(self):
        """ returns true if the activity is a subflow  """
        return self.kind == 'subflow'


    security.declareProtected('Manage OpenFlow', 'isDummy')
    def isDummy(self):
        """ returns true if the activity is a dummy  """
        return self.kind == 'dummy'


    security.declareProtected('Manage OpenFlow', 'isAutoPush')
    def isAutoPush(self):
        """ returns true if the activity push mode is automatic"""
        return self.auto_push_mode and self.kind=='standard'


    security.declareProtected('Manage OpenFlow', 'editPushRoles')
    def editPushRoles(self, roles):
        """ edit push permission roles list """
        self._push_roles = roles


    security.declareProtected('Manage OpenFlow', 'getPushRoles')
    def getPushRoles(self):
        """ return push permission roles list """
        return self._push_roles

    security.declareProtected('Manage OpenFlow', 'editPullRoles')
    def editPullRoles(self, roles):
        """ edit pull permission roles list """
        self._pull_roles = roles


    security.declareProtected('Manage OpenFlow', 'getPullRoles')
    def getPullRoles(self):
        """ return pull permission roles list """
        return self._pull_roles


    security.declareProtected('Manage OpenFlow', 'editPushPermissionsRoles')
    def editPushPermissionsRoles(self, roles):
        """ edit push permission roles list """

        self.editPushRoles(roles)

        catalog = getattr(self, 'Catalog')
        if catalog:
            results = catalog.searchResults(meta_type='Workitem',
                                            activity_id=self.id,
                                            process_id=self.aq_parent.id)
            for workitem_brain in results:
                workitem = workitem_brain.getObject()
                workitem.push_roles = self._push_roles


    security.declareProtected('Manage OpenFlow', 'editPullPermissionsRoles')
    def editPullPermissionsRoles(self, roles=[]):
        """ edit pull permission roles list """

        self.editPullRoles(roles)

        catalog = getattr(self, 'Catalog')
        if catalog:
            results = catalog.searchResults(meta_type='Workitem',
                                            activity_id=self.id,
                                            process_id=self.aq_parent.id)
            for workitem_brain in results:
                workitem = workitem_brain.getObject()
                workitem.pull_roles = self._pull_roles


    security.declareProtected('Manage OpenFlow', 'editPermissionsRoles')
    def editPermissionsRoles(self, REQUEST=None):
        """ edit permission roles list """
        from string import split

        if REQUEST:
            form = REQUEST.form
            push_roles = []
            pull_roles = []
            for permission_role in form.keys():
                permission, role = split(permission_role, '%')
                if form[permission_role]=='on':
                    if permission=='push':
                        push_roles.append(role)
                    else:
                        pull_roles.append(role)

            self.editPushPermissionsRoles(push_roles)
            self.editPullPermissionsRoles(pull_roles)
            return REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)
