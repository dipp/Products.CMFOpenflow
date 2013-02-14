from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from OFS.Folder import Folder, manage_addFolder
from DateTime import DateTime
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware
from activity import activity
from transition import transition
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Globals import package_home


def manage_addProcess(self,
                      id,
                      title="",
                      description="",
                      BeginEnd=None,
                      priority=0,
                      limit=0,
                      valid_from=0,
                      valid_to=0,
                      waiting_time=0,
                      duration=0,
                      duration_unit='days',
                      REQUEST=None):
    """ adds a new process """
    p = process(id,
                title,
                description,
                BeginEnd,
                priority,
                limit,
                valid_from,
                valid_to,
                waiting_time,
                duration,
                duration_unit)
    self._setObject(id, p)


manage_addProcessForm = PageTemplateFile('zpt/openflow/manage_addProcessForm', globals())


class process(CatalogPathAware, Folder):
    """ A process is a collection of activities and transitions.
    The process map is given by the linking of activities by transitions.
    Each process instance is described by a instance"""

    def __init__(self,
                 id,
                 title="",
                 description="",
                 BeginEnd=None,
                 priority=0,
                 limit=0,
                 valid_from=0,
                 valid_to=0,
                 waiting_time=0,
                 duration=0,
                 duration_unit='days'):
        self.id = id
        self.title = title
        self.description = description
        self.created = DateTime()
        self.priority = priority
        self.limit = limit
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.waiting_time = waiting_time
        self.duration = duration
        self.duration_unit = duration_unit
        if BeginEnd:
            self.addActivity('Begin', kind='dummy')
            self.addActivity('End', kind='dummy')
            self.begin = 'Begin'
            self.end = 'End'
        else:
            self.begin = ''
            self.end = ''


    security = ClassSecurityInfo()


    security.declareProtected('Manage OpenFlow', 'manage_addActivityForm')
    manage_addActivityForm = PageTemplateFile('zpt/process/manage_addActivityForm', globals())


    security.declareProtected('Manage OpenFlow', 'manage_addTransitionForm')
    manage_addTransitionForm = PageTemplateFile('zpt/process/manage_addTransitionForm', globals())


    security.declareProtected('Manage OpenFlow', 'index_html')
    index_html = PageTemplateFile('zpt/process/Map', globals())


    security.declareProtected('Manage OpenFlow', 'Setting')
    Setting = PageTemplateFile('zpt/process/Setting', globals())


    meta_type = 'Process'


    manage_options = ({'label' : 'Map', 'action' : 'index_html'},
                      {'label' : 'Setting', 'action' : 'Setting'}
                      ) + Folder.manage_options[0:1] + Folder.manage_options[2:]


    security.declareProtected('Manage OpenFlow', 'edit')
    def edit(self,
             begin=None,
             end=None,
             title=None,
             description=None, 
             priority=None,
             limit=None,
             valid_from=None,
             valid_to=None,
             waiting_time=None,
             duration=None,
             duration_unit=None,
             REQUEST=None):
        """ changes the process settings """
        if title:
            self.title = title
        if description:
            self.description = description
        if begin:
            self.begin = begin
        if end:
            self.end = end
        if priority:
            self.priority = priority
        if limit:
            self.limit = limit
        if valid_from:
            self.valid_from = valid_from
        if valid_to:
            self.valid_to = valid_to
        if waiting_time:
            self.waiting_time = waiting_time
        if duration:
            self.duration = duration
        if duration_unit:
            self.duration_unit = duration_unit
        if REQUEST:
            return self.Setting(self,REQUEST,manage_tabs_message="Changed")


    security.declareProtected('Manage OpenFlow', 'addActivity')
    def addActivity(self,
                    id,
                    split_mode='and',
                    join_mode='and',
                    auto_push_mode=0,
                    start_mode=0,
                    finish_mode=0,
                    subflow='',
                    push_application='',
                    application='',
                    title='',
                    parameters='',
                    description='',
                    limit=0,
                    kind = 'standard',
                    REQUEST=None):
        """ adds the activity """
        a = activity(id=id,
                     process_id=self.id,
                     join_mode=join_mode,
                     split_mode=split_mode,
                     auto_push_mode=auto_push_mode,
                     start_mode=start_mode,
                     finish_mode=finish_mode,
                     subflow=subflow,
                     push_application=push_application,
                     application=application,
                     title=title,
                     parameters=parameters,
                     description=description,
                     limit=limit,
                     kind=kind)
        self._setObject(id, a)
        if REQUEST: REQUEST.RESPONSE.redirect('index_html')


    security.declareProtected('Manage OpenFlow', 'addTransition')
    def addTransition(self, id, From, To, condition=None, REQUEST=None):
        """ adds a transition """
        t = transition(id, From, To, condition)
        self._setObject(t.id, t)
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Manage OpenFlow', 'manage_delObjects')
    def manage_delObjects(self, ids=[], REQUEST=None):
      """ override default method to handle better the redirection """
      Folder.manage_delObjects(self, ids)
      if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)

    def manage_afterAdd(self, item, container):
      for activity in self.objectValues('Activity'):
        activity.process_id=self.id
        activity.index_object()
      for transition in self.objectValues('Transition'):
        transition.index_object()
      self.index_object()

InitializeClass(process)
