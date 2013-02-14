from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from OFS.Folder import Folder
from DateTime import DateTime
from Products.ZCatalog.ZCatalog import ZCatalog
from instance import instance
from process import process
from expression import exprNamespace
from Products.CMFCore.Expression import Expression, createExprContext
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from zLOG import LOG, ERROR, INFO


def manage_addOpenflow(self, id, RESPONSE=None):
    """ adds openflow_tool in the portal """
    w = CMFOpenflowTool(id)
    self._setObject(id, w)
    if RESPONSE is not None:
        RESPONSE.redirect('manage_main')


manage_addOpenflowForm = PageTemplateFile('zpt/openflow/manage_addOpenFlowForm', globals())


class CMFOpenflowTool(UniqueObject, Folder, ActionProviderBase):
    """ A CMFOpenflowTool folder contains all the workflow objects and API """


    def __init__(self, id='portal_openflow'):
        self.id = id
        self._applications = {} #{'application_id':{'url':'application_url'},...}

        catalog = ZCatalog('Catalog', 'Default OpenFlow Catalog')

        try:
          # For ZCatalog 2.2.0
          catalog.addIndex('id', 'FieldIndex')
          catalog.addColumn('id')

          catalog.addIndex('meta_type', 'FieldIndex')
          catalog.addColumn('meta_type')
        except:
          pass

        catalog.addIndex('description', 'FieldIndex')
        catalog.addColumn('description')

        catalog.addIndex('customer', 'FieldIndex')
        catalog.addColumn('customer')

        catalog.addIndex('creation_time', 'FieldIndex')
        catalog.addColumn('creation_time')

        catalog.addIndex('priority', 'FieldIndex')
        catalog.addColumn('priority')

        catalog.addIndex('status', 'FieldIndex')
        catalog.addColumn('status')

        catalog.addIndex('From', 'FieldIndex')
        catalog.addColumn('From')

        catalog.addIndex('To', 'FieldIndex')
        catalog.addColumn('To')

        catalog.addIndex('activity_id', 'FieldIndex')
        catalog.addColumn('activity_id')

        catalog.addIndex('process_id', 'FieldIndex')
        catalog.addColumn('process_id')

        catalog.addIndex('instance_id', 'FieldIndex')
        catalog.addColumn('instance_id')

        catalog.addIndex('workitems_from', 'FieldIndex')
        catalog.addColumn('workitems_from')

        catalog.addIndex('workitems_to', 'FieldIndex')
        catalog.addColumn('workitems_to')

        catalog.addIndex('actor', 'FieldIndex')
        catalog.addColumn('actor')

        catalog.addIndex('push_roles', 'KeywordIndex')
        catalog.addColumn('push_roles')

        catalog.addIndex('pull_roles', 'KeywordIndex')
        catalog.addColumn('pull_roles')

        self._setObject('Catalog', catalog)


    security = ClassSecurityInfo()


    security.declareObjectProtected('Use OpenFlow')


    security.declareProtected('Manage OpenFlow', 'manage_addApplicationForm')
    manage_addApplicationForm = PageTemplateFile('zpt/openflow/manage_addApplicationForm', globals())


    security.declareProtected('Manage OpenFlow', 'manage_editApplicationForm')
    manage_editApplicationForm = PageTemplateFile('zpt/openflow/manage_editApplicationForm', globals())


    security.declareProtected('Manage OpenFlow', 'manage_addInstanceForm')
    manage_addInstanceForm = PageTemplateFile('zpt/openflow/manage_addInstanceForm', globals())


    security.declareProtected('Manage OpenFlow', 'manage_addProcessForm')
    manage_addProcessForm = PageTemplateFile('zpt/openflow/manage_addProcessForm', globals())


    security.declareProtected('Manage OpenFlow', 'Applications')
    Applications = PageTemplateFile('zpt/openflow/Applications', globals())


    security.declareProtected('Use OpenFlow', 'index_html')
    index_html =  PageTemplateFile('zpt/openflow/WorkList', globals())


    security.declareProtected('Manage OpenFlow', 'Processes')
    Processes = PageTemplateFile('zpt/openflow/Processes', globals())


    security.declareProtected('Manage OpenFlow', 'Instances')
    Instances = PageTemplateFile('zpt/openflow/Instances', globals())


    security.declareProtected('Use OpenFlow', 'manage_pushWorkitem')
    manage_pushWorkitem = PageTemplateFile('zpt/openflow/manage_pushWorkitem', globals())


    security.declareProtected('Manage OpenFlow', 'manage_chooseFallin')
    manage_chooseFallin = PageTemplateFile('zpt/openflow/manage_chooseFallin', globals())

    
    meta_type = 'CMF OpenFlow Tool'


    manage_options = ({'label': 'Worklist',
                       'action': 'index_html',
                       'help' : ('CMFOpenFlowTool', 'openflow.stx')},
                      {'label': 'Applications',
                       'action': 'Applications',
                       'help' : ('CMFOpenFlowTool', 'applications.stx')},
                      {'label': 'Process definitions',
                       'action': 'Processes',
                       'help' : ('CMFOpenFlowTool', 'processes.stx')},
                      {'label':'Process instances',
                       'action':'Instances',
                       'help' : ('CMFOpenFlowTool', 'processes.stx')},
                      {'label':'Management',
                       'action':'Management'}) + \
                       Folder.manage_options[0:1] + Folder.manage_options[2:]


    security.declareProtected('Use OpenFlow', 'usersAssignableTo')
    def usersAssignableTo(self, process_id, activity_id, object=None):
        """ List all user name assignable to activity in the process """
        activity = getattr(getattr(self,process_id),activity_id)
        result=[]
        if not object:
          object=self
        current=object
        while current is not None:
            if hasattr(current, 'acl_users'):
                for user in getattr(current, 'acl_users').getUsers():
                    name = user.getUserName()
                    roles = user.getRolesInContext(object) #
                    if name not in result and [r for r in roles if r in activity.getPullRoles()]:
                        result.append(name)
            try:
                current = current.aq_parent
            except:
                current = None
        return result


    security.declareProtected('Manage OpenFlow', 'addProcess')
    def addProcess(self,
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
        if REQUEST: REQUEST.RESPONSE.redirect('Processes')


    security.declareProtected('Manage OpenFlow', 'deleteProcess')
    def deleteProcess(self, proc_ids=None, REQUEST=None):
        """ removes specified process """
        self.manage_delObjects(proc_ids)
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'addInstance')
    def addInstance(self, process_id, customer, comments, title, activation=0, priority=0, REQUEST=None):
        """ adds an a process definition instance """
        begin_activity_id = getattr(self, process_id).begin
        i = instance(process_id, begin_activity_id, customer, title, comments, priority)
        self._setObject(i.id, i)
        if activation:
            self.startInstance(i.id)
        if REQUEST:
            REQUEST.RESPONSE.redirect('Instances')
        else:
            return i.id


    security.declareProtected('Manage OpenFlow', 'deleteInstance')
    def deleteInstance(self, inst_ids=None, REQUEST=None):
        """ removes specified instances"""
        remove_list = []
        for id in inst_ids:
            instance = getattr(self, id)
            if instance.status in ['complete', 'terminated']:
                remove_list.append(instance.id)
        self.manage_delObjects(remove_list)
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Manage OpenFlow', 'suspendInstance')
    def suspendInstance(self, instance_id=None, REQUEST=None):
        """ suspend a specified instance """
        instance = getattr(self, instance_id)
        if instance.isActiveOrRunning() or instance.status == 'initiated':
            if REQUEST:
                actor=REQUEST.AUTHENTICATED_USER.getUserName()
            else:
                actor='Engine'
            instance.old_status = instance.status
            instance.setStatus(status='suspended', actor=actor)
        else:
            raise "InstanceActionError","Instance in wrong status"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Manage OpenFlow', 'suspendInstance')
    def resumeInstance(self, instance_id=None, REQUEST=None):
        """ suspend a specified instance """
        instance = getattr(self, instance_id)
        if instance.status == 'suspended':
            if REQUEST:
                actor=REQUEST.AUTHENTICATED_USER.getUserName()
            else:
                actor='Engine'
            instance.setStatus(status=instance.old_status, actor=actor)
            instance.old_status = ''
        else:
            raise "InstanceActionError","Instance in wrong status"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Manage OpenFlow', 'terminateInstance')
    def terminateInstance(self, instance_id=None, REQUEST=None):
        """ terminate a specified instance """
        instance = getattr(self, instance_id)
        if instance.status != 'complete':
            if REQUEST:
                actor=REQUEST.AUTHENTICATED_USER.getUserName()
            else:
                actor='Engine'
            instance.setStatus(status='terminated', actor=actor)
        else:
            raise "InstanceActionError","Instance in wrong status"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'startInstance')
    def startInstance(self, instance_id, REQUEST=None):
        """ Starts the flowing of the process instance inside the process definition """
        instance = getattr(self, instance_id)
        if instance.status == 'initiated':
            if REQUEST:
                actor=REQUEST.AUTHENTICATED_USER.getUserName()
            else:
                actor='Engine'
            instance.setStatus(status='running', actor=actor)
            process_id = instance.begin_process_id
            activity_id = instance.begin_activity_id
            push_roles = getattr(getattr(self,process_id),activity_id).getPushRoles()
            pull_roles = getattr(getattr(self,process_id),activity_id).getPullRoles()
            w = instance.addWorkitem(process_id, activity_id, 0, push_roles, pull_roles)
            self.manageWorkitemCreation(instance_id, w.id)
            if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)
        else:
            raise "InstanceActionError","Instance in wrong status"


    def linkWorkitems(self, instance_id, workitem_from_id, workitem_to_id_list):
        instance = getattr(self, instance_id)
        workitem_from = getattr(instance, workitem_from_id)
        workitem_from.addTo(workitem_to_id_list)
        for w_id in workitem_to_id_list:
            w = getattr(instance, w_id)
            w.addFrom(workitem_from_id)
            w.setGraphLevel(workitem_from.graph_level + 1)


    security.declareProtected('Manage OpenFlow', 'addApplication')
    def addApplication(self, name, link, REQUEST=None):
        """ adds an application declaration """
        if not name in self._applications.keys():
            self._applications[name] = {'url' : link}
            self._p_changed = 1
            if REQUEST:
                REQUEST.RESPONSE.redirect('Applications')


    security.declareProtected('Manage OpenFlow', 'deleteApplication')
    def deleteApplication(self, app_ids=None, REQUEST=None):
        """ removes an application """
        for name in app_ids:
            if name in self._applications.keys():
                del(self._applications[name])
        self._p_changed = 1
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Manage OpenFlow', 'editApplication')
    def editApplication(self, name, link, REQUEST=None):
        """ edits an application declaration """
        if name not in self._applications.keys():
            return
        self._applications[name] = {'url' : link}
        self._p_changed = 1
        if REQUEST:
            REQUEST.RESPONSE.redirect('Applications')


    security.declareProtected('Use OpenFlow', 'listApplications')
    def listApplications(self):
        """ List application declaration;
        returns a list of dictionaries with keys: name, link """
        return map(lambda x, self=self: {'name' : x,
                                         'link' : self._applications[x]['url']},
                                         self._applications.keys())


    security.declareProtected('Use OpenFlow', 'getApplicationUrl')
    def getApplicationUrl(self, instance_id, workitem_id):
        """ Return application definition URL relative to instance and workitem"""
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        application = activity.application
        if application in self._applications.keys():
            return self._applications[application]['url']
        else:
            return ""

    security.declareProtected('Use OpenFlow', 'getApplicationUrlWithParameters')
    def getApplicationUrlWithParameters(self, instance_id, workitem_id):
        """ Return application definition URL relative to instance and workitem with parameters"""
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        application = activity.application
        if application in self._applications.keys():
            url = '%s?instance_id=%s&workitem_id=%s&process_id=%s&activity_id=%s' % (
                self._applications[application]['url'],
                instance.id,
                workitem.id,
                process.id,
                activity.id)
            return url
        else:
            return ""


    def getEnvironment(self, instance_id, workitem_id):
        instance = getattr(self, instance_id)
        workitem = getattr(instance, workitem_id)
        process_id = workitem.process_id
        activity_id = workitem.activity_id
        process = getattr(self, process_id)
        activity = getattr(process, activity_id)
        return instance, workitem, process, activity


    security.declareProtected('Use OpenFlow', 'getInstanceAndWorkitem')
    def getInstanceAndWorkitem(self, instance_id, workitem_id):
        """ return the objects requested """
        instance = getattr(self, instance_id)
        workitem = getattr(instance, str(workitem_id))
        return instance, workitem

    security.declareProtected('Use OpenFlow', 'assignWorkitem')
    def assignWorkitem(self, instance_id, workitem_id, actor, REQUEST=None):
        """ Assign the specified workitem of the specified instance to the specified actor (string)"""
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        if REQUEST:
            if [r for r in REQUEST.AUTHENTICATED_USER.getRolesInContext(self) if r in workitem.push_roles]:
                if instance.isActiveOrRunning() and not workitem.status == 'completed' and workitem.actor=='':
                    # check if actor is assignable to workitem's activity
                    workitem.assignTo(actor)
                else:
                    raise "WorkitemActionError","Wrong workitem enviroment"
        else:
            if instance.isActiveOrRunning() and not workitem.status == 'completed' and workitem.actor == '':
                workitem.assignTo(actor)
            else:
                raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'selfAssignWorkitem')
    def selfAssignWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ Assign the specified workitem of the specified instance to the user"""
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        if REQUEST:
            if [r for r in REQUEST.AUTHENTICATED_USER.getRolesInContext(self) if r in workitem.pull_roles]:
                if instance.isActiveOrRunning() and not workitem.status == 'completed' and workitem.actor=='':
                    workitem.assignTo(REQUEST.AUTHENTICATED_USER.getUserName())
                else:
                    raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'unassignWorkitem')
    def unassignWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ Unassign the specified workitem """
        instance = getattr(self, instance_id)
        workitem = getattr(instance, str(workitem_id))
        if REQUEST:
            if not [r for r in REQUEST.AUTHENTICATED_USER.getRolesInContext(self) if r in workitem.push_roles]:
                raise "PermissionError","User don't have push role"
        if instance.isActiveOrRunning() and workitem.status != 'completed':
            getattr(instance, workitem_id).assignTo('')
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'activateWorkitem')
    def activateWorkitem(self, instance_id, workitem_id, actor=None, REQUEST=None):
        """ declares the activation of the specified workitem of the given instance """
        instance = getattr(self, instance_id)
        workitem = getattr(instance, str(workitem_id))
        if REQUEST:
            action_actor=REQUEST.AUTHENTICATED_USER.getUserName()
            if not [r for r in REQUEST.AUTHENTICATED_USER.getRolesInContext(self) if r in workitem.pull_roles]:
                raise "PermissionError","User don't have pull role"
        else:
            action_actor='Engine'
        if instance.isActiveOrRunning() and workitem.status == 'inactive' and not workitem.blocked:
            if actor is not None and workitem.actor == '':
                self.assignWorkitem(instance_id, workitem_id, actor)
            workitem.setStatus('active', actor=action_actor)
            if instance.status!='active':
              instance.setStatus(status='active', actor=action_actor)
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'inactivateWorkitem')
    def inactivateWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ declares the inactivation of the specified workitem of the given instance """
        instance = getattr(self, instance_id)
        workitem = getattr(instance, str(workitem_id))
        if REQUEST:
            actor=REQUEST.AUTHENTICATED_USER.getUserName()
        else:
            actor='Engine'
        if REQUEST:
            if not (actor == workitem.actor or \
               REQUEST.AUTHENTICATED_USER.has_permission('Manage OpenFlow', self)):
                raise "WorkitemActionError","Invalid actor"
        if instance.isActiveOrRunning() and workitem.status == 'active' and not workitem.blocked:
            workitem.setStatus('inactive', actor=actor)
            if instance.getActiveWorkitems() == 0 and instance.status!='running':
                instance.setStatus(status='running', actor=actor)
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'suspendWorkitem')
    def suspendWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ declares the suspension of the specified workitem of the given instance """
        instance = getattr(self, instance_id)
        workitem = getattr(instance, str(workitem_id))
        if REQUEST:
            actor = REQUEST.AUTHENTICATED_USER.getUserName()
        else:
            actor = 'Engine'
        if REQUEST:
            if  workitem.actor and workitem.actor != actor:
                raise "Invalid Workflow Actor: %s"%actor
        if instance.isActiveOrRunning() and workitem.status == 'inactive' and not workitem.blocked:
            workitem.setStatus('suspended', actor=actor)
            if instance.getActiveWorkitems() == 0 and not instance.status=='running':
                instance.setStatus(status='running', actor=actor)
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'resumeWorkitem')
    def resumeWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ declares the resumption of the specified workitem of the given instance """
        instance = getattr(self, instance_id)
        workitem = getattr(instance, str(workitem_id))
        if REQUEST:
            actor = REQUEST.AUTHENTICATED_USER.getUserName()
        else:
            actor = 'Engine'
        if REQUEST:
            if not actor == workitem.actor:
                raise "Invalid Workflow Actor"
        if instance.isActiveOrRunning() and workitem.status == 'suspended' and not workitem.blocked:
            workitem.setStatus('inactive', actor=actor)
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'completeWorkitem')
    def completeWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ declares the completion of the specified workitem of the given instance """
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        if REQUEST:
            actor = REQUEST.AUTHENTICATED_USER.getUserName()
        else:
            actor = 'Engine'
        if REQUEST:
            if not actor == workitem.actor:
                raise "WorkitemActionError","Invalid Workflow Actor"
        if instance.isActiveOrRunning():
            workitem_return_id = None
            if workitem.status in ('active', 'fallout'):
                workitem.setStatus('complete', actor=actor)
                if instance.getActiveWorkitems() == 0 and instance.status!='running':
                    instance.setStatus(status='running', actor=actor)
                if self.isEnd(workitem.process_id, workitem.activity_id):
                    subflow_workitem_id = self.getSubflowWorkitem(instance_id, workitem_id, workitem.process_id)
                    if subflow_workitem_id:
                        self.completeSubflow(instance_id, subflow_workitem_id)
                    else:
                        instance.setStatus(status='complete', actor=actor)
            if activity.isAutoFinish() and not process.end == activity.id and \
               not (activity.kind=='dummy' or activity.kind=='subflow'):
                self.forwardWorkitem(instance_id, workitem_id)
            if REQUEST is not None: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"


    def isEnd(self, process_id, activity_id):
        process = getattr(self, process_id)
        return process.end == activity_id


    security.declareProtected('Use OpenFlow', 'getNextTransitions')
    def getNextTransitions(self, instance_id, workitem_id):
        """ Returns the list of transition that the given workitem (of the specified instance)
        will be routed on"""
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        transition_list = []
        split_mode = activity.split_mode
        activity_outgoing_transitions = filter(lambda x, activity_id=activity.id : x.From==activity_id, process.objectValues('Transition'))
        transition_condition_list = map(lambda x : {'transition_id' : x.id, 'condition' : x.condition}, activity_outgoing_transitions)
        if len(transition_condition_list) == 1:
            transition_list = [transition_condition_list[0]['transition_id']]
        else:
            if split_mode == 'and':
                transition_list = map(lambda x : x['transition_id'], transition_condition_list)
            elif split_mode == 'xor':
                for r in transition_condition_list:
                    expr=Expression(r['condition'])
                    ec=exprNamespace(object=instance)
                    if expr(ec):
                        transition_list = [r['transition_id']]
                        break
        return transition_list


    security.declareProtected('Use OpenFlow', 'getDestinations')
    def getDestinations(self, instance_id, workitem_id, path=None):
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        if path:
            transition_list = [path]
        else:
            transition_list = self.getNextTransitions(instance_id, workitem_id)
            if transition_list==[] and process.end!=workitem.activity_id:
               raise "OpenflowNoRoute", "Workflow erroneous. The process don't know what to do now (no transitions to follow for this instance)." + str(transition_list)
        destinations = []
        for transition_id in transition_list:
            activity_to_id = getattr(process, transition_id).To
            activity_to = getattr(process, activity_to_id)
            if getattr(process, activity_to_id).join_mode=='and':
                blocked_init = activity_to.getIncomingTransitionsNumber() - 1
            else:
                blocked_init = 0

            destinations.append({'activity_to_id' : activity_to_id,
                                 'blocked_init' : blocked_init,
                                 'process_to_id' : process.id})
        return destinations


    security.declareProtected('Use OpenFlow', 'getPath')
    """ Useful to help manual routing, returns the activities in which a workitem can be forwarded """
    def getPath(self, instance_id, workitem_id, path=None):
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        if path:
            transition_list = [path]
        else:
            transition_list = self.getNextTransitions(instance_id, workitem_id)
            if transition_list==[]:
               # FIX-ME vds:create custom exception
               raise "OpenflowNoRoute", "Workflow erroneous. The process don't know what to do now (no transitions to follow for this instance)."
        destinations = []
        for transition_id in transition_list:

            activity_to_id = getattr(process, transition_id).To
            activity_to = getattr(process, activity_to_id)
            destinations.append({'activity_to_id': activity_to_id,
                                 'process_to_id': process.id,
                                 'transition_to_id':transition_id})
        return destinations


    security.declareProtected('Use OpenFlow', 'forwardWorkitem')
    def forwardWorkitem(self, instance_id, workitem_id, path=None, REQUEST=None):
        """ instructs openflow to forward the specified workitem """
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        if REQUEST:
            if not REQUEST.AUTHENTICATED_USER.getUserName() == workitem.actor:
                raise "WorkitemActionError","Invalid Workflow Actor"
        destinations = self.getDestinations(instance_id, workitem_id, path)
        new_workitems = []
        if instance.isActiveOrRunning() and \
          (workitem.status == 'complete' and not workitem.forwarded) and \
          not self.isEnd(workitem.process_id, workitem.activity_id):
            activity_to_id_list = map(lambda x : x['activity_to_id'], destinations)
            workitem.addEvent('forwarded to '+ reduce(lambda x, y : x+', '+y, activity_to_id_list))
            workitem_to_id_list = []
            for d in destinations:
                w = instance.getJoiningWorkitem(workitem_id, self)
                if w:
                    w.unblock()
                    workitem_to_id_list.append(w.id)
                else:
                    process_id = d['process_to_id']
                    activity_id = d['activity_to_id']
                    push_roles = getattr(getattr(self,process_id),activity_id).getPushRoles()
                    pull_roles = getattr(getattr(self,process_id),activity_id).getPullRoles()
                    w = instance.addWorkitem(process_id,
                                             activity_id,
                                             d['blocked_init'],
                                             push_roles,
                                             pull_roles)
                    workitem_to_id_list.append(w.id)
                if w.blocked == 0:
                    new_workitems.append(w.id)
                    w.addEvent('arrival from ' + workitem.activity_id)
            # indented with for

            self.linkWorkitems(instance_id, workitem_id, workitem_to_id_list)
        elif (workitem.status == 'complete' and not workitem.forwarded) and \
             self.isEnd(workitem.process_id, workitem.activity_id):
            pass
        else:
            msg=" wid: "+workitem.id+" act_id: "+workitem.activity_id
            msg=msg+" status:"+workitem.status+" forwarded:"+str(workitem.forwarded)
            raise "WorkitemActionError","Wrong workitem enviroment"+msg
        for w in new_workitems:
            self.manageWorkitemCreation(instance_id, w)
        workitem.forwarded=1
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'falloutWorkitem')
    def falloutWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ drops the workitem (of the specified instance) in exceptional handling """
        instance = getattr(self, instance_id)
        workitem = getattr(instance, workitem_id)
        if REQUEST:
            actor = REQUEST.AUTHENTICATED_USER.getUserName()
        else:
            actor = 'Engine'
        if REQUEST:
            if actor != workitem.actor and \
               [r for r in REQUEST.AUTHENTICATED_USER.getRolesInContext(self) if r in workitem.push_roles]==[]:
              raise "WorkitemActionError","Invalid Workflow Actor"
        if not workitem.blocked:
            workitem.setStatus('fallout', actor=actor)
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Manage OpenFlow', 'fallinWorkitem')
    def fallinWorkitem(self, instance_id, workitem_id, process_id, activity_id, REQUEST=None, coming_from=None):
        """ the exceptional specified workitem (of the specified instance) will be put back in the activity
        specified by process_id and activity_id; workitem will still be in exceptional state:
        use endFallinWorkitem API to specify the end of the exceptional state"""
        instance = getattr(self, instance_id)
        workitem_from = getattr(instance, workitem_id)
        if workitem_from.status=='fallout':
            push_roles = getattr(getattr(self,process_id),activity_id).getPushRoles()
            pull_roles = getattr(getattr(self,process_id),activity_id).getPullRoles()
            workitem_to = instance.addWorkitem(process_id, activity_id, 0, push_roles, pull_roles)
            self.linkWorkitems(instance_id, workitem_id, [workitem_to.id])
            event = 'fallin to activity ' + activity_id + ' in process ' + process_id + \
                    ' (workitem ' + str(workitem_to.id) + ')'
            workitem_from.addEvent(event)
            event = 'fallin from activity ' + workitem_from.activity_id + \
                    ' in process ' + workitem_from.process_id + \
                    ' (workitem ' + str(workitem_id) + ')'
            workitem_to.addEvent(event)
            self.manageWorkitemCreation(instance_id, workitem_to.id)
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST:
            if coming_from is not None:
                REQUEST.RESPONSE.redirect(coming_from)
            else:
                REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Manage OpenFlow', 'endFallinWorkitem')
    def endFallinWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ ends the exceptional state of the given workitem (of the specified instance) """
        instance = getattr(self, instance_id)
        workitem = getattr(instance, workitem_id)
        if workitem.status=='fallout':
            workitem.addEvent('handled fallout')
            if not filter(lambda x: x['event'] == 'complete', workitem.getEventLog()):
                workitem.endFallin()
        else:
            raise "WorkitemActionError","Wrong workitem enviroment"
        if REQUEST: REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)


    security.declareProtected('Use OpenFlow', 'manageDummyActivity')
    def manageDummyActivity(self, instance_id, workitem_id):
        """  """
        self.activateWorkitem(instance_id, workitem_id, 'Engine')
        self.completeWorkitem(instance_id, workitem_id)
        self.forwardWorkitem(instance_id, workitem_id)



    security.declareProtected('Use OpenFlow', 'startAutomaticApplication')
    def startAutomaticApplication(self, instance_id, workitem_id):
        """  """
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        application_url = self.getApplicationUrl(instance_id,workitem_id)
        parameters = {'instance_id':instance.id,
                      'workitem_id':workitem.id,
                      'process_id':process.id,
                      'activity_id':activity.id}
        if application_url:
            # application should have the parameter keys in parameters
            apply(self.restrictedTraverse(application_url),(),parameters)
        self.activateWorkitem(instance_id, workitem_id, 'Engine')
        self.completeWorkitem(instance_id, workitem_id)


    security.declarePrivate('callAutoPush')
    def callAutoPush(self, instance_id, workitem_id, REQUEST=None):
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        application_id = activity.push_application
        parameters = {'instance_id':instance.id,
                      'workitem_id':workitem.id,
                      'process_id':process.id,
                      'activity_id':activity.id}
        if application_id:
            application_url = self._applications[application_id]['url']
            actor = apply(self.restrictedTraverse(application_url),(),parameters)
            self.assignWorkitem(instance_id, workitem_id, actor)


    security.declarePrivate('startSubflow')
    def startSubflow(self, instance_id, workitem_id, REQUEST=None):
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        self.activateWorkitem(instance_id, workitem_id)
        self.assignWorkitem(instance_id, workitem_id, 'Engine')
        subflow_id = activity.subflow
        begin_activity_id = getattr(self, subflow_id).begin
        push_roles = getattr(getattr(self,process.id),activity.id).getPushRoles()
        pull_roles = getattr(getattr(self,process.id),activity.id).getPullRoles()
        w = instance.addWorkitem(subflow_id, begin_activity_id, 0, push_roles, pull_roles)
        self.linkWorkitems(instance_id, workitem_id, [w.id])
        self.manageWorkitemCreation(instance_id, w.id)


    def getSubflowWorkitem(self, instance_id, workitem_id, subflow_id):
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        if activity.isSubflow() and activity.subflow==subflow_id and workitem.status=='active':
            return workitem_id
        elif workitem.workitems_from == []:
            #raise exception?
            return None
        else:
            return self.getSubflowWorkitem(instance_id, workitem.workitems_from[0], subflow_id)


    def completeSubflow(self, instance_id, workitem_id):
        self.completeWorkitem(instance_id, workitem_id)
        self.forwardWorkitem(instance_id, workitem_id)


    def manageWorkitemCreation(self, instance_id, workitem_id):
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        if instance.status in ('active', 'running'):
            if activity.isDummy():
                self.manageDummyActivity(instance_id, workitem_id)
            if activity.isAutoPush():
                self.callAutoPush(instance_id, workitem_id)
            if activity.isAutoStart():
                self.startAutomaticApplication(instance_id, workitem_id)
            if activity.isSubflow():
                self.startSubflow(instance_id, workitem_id)


    security.declareProtected('Use OpenFlow', 'countWorkitems')
    def countWorkitems(self, process_id=None, activity_id=None, actor=None):
        """  Count the number of workitem """
        #toDo: workitems assigned
        #toAssign: workitems not yet assigned
        #completed: workitems completed
        catalog = self.Catalog
        toDo, toAssign, completed= (0, 0, 0)
        instances = self.objectValues('Instance')
        result=[]
        for i in instances:
            result = result+i.objectValues('Workitem')

        if process_id and not activity_id and not actor:
            toDo = len([w for w in result
                       if w.process_id==process_id and
                          w.actor!='' and
                         (w.status=='active' or w.status=='inactive')])
            toAssign = len([w for w in result if w.process_id==process_id and w.actor==''])
            completed = len([w for w in result if w.process_id==process_id and w.status=='complete'])
        elif process_id and not activity_id and actor:
            toDo = len([w for w in result
                       if w.process_id==process_id and
                          w.actor==actor and
                         (w.status=='active' or w.status=='inactive')])
            toAssign = len([w for w in result if w.process_id==process_id and w.actor==''])
            completed = len([w for w in result
                            if w.process_id==process_id and
                               w.actor==actor and
                               w.status=='complete'])
        elif process_id and activity_id and not actor:
            toDo = len([w for w in result
                       if w.process_id==process_id and
                          w.activity_id==activity_id and
                          w.actor!='' and
                         (w.status=='active' or w.status=='inactive')])
            toAssign = len([w for w in result
                            if w.process_id==process_id and
                               w.activity_id==activity_id and
                               w.actor==''])
            completed = len([w for w in result
                            if w.process_id==process_id and
                               w.activity_id==activity_id and
                               w.status=='complete'])
        elif process_id and activity_id and actor:
            toDo = len([w for w in result
                       if w.process_id==process_id and
                          w.activity_id==activity_id and
                          w.actor==actor and
                         (w.status=='active' or w.status=='inactive')])
            toAssign = len([w for w in result
                            if w.process_id==process_id and
                               w.activity_id==activity_id and
                               w.actor==''])
            completed = len([w for w in result
                            if w.process_id==process_id and
                               w.activity_id==activity_id and
                               w.actor==actor and
                               w.status=='complete'])
        else:
            toDo = len([w for w in result
                       if w.actor!='' and
                         (w.status=='active' or w.status=='inactive')])
            toAssign = len([w for w in result if w.actor==''])
            completed = len([w for w in result if w.status=='complete'])
        return {'to do':str(toDo), 'to assign':str(toAssign), 'completed':str(completed)}


    security.declareProtected('Use OpenFlow', 'getUserActionsOnWorkitem')
    def getUserActionsOnWorkitem(self, instance_id, workitem_id, REQUEST=None):
        """ Return the actions that user can do on the workitem (filtered on permissions only)"""
        instance, workitem, process, activity = self.getEnvironment(instance_id, workitem_id)
        actions = {} # { action_name:action_url, ...}
        absolute_url = self.absolute_url()
        parameters = '?instance_id=%s&workitem_id=%s'%(instance_id, workitem_id)
        user_name = REQUEST.AUTHENTICATED_USER.getUserName()
        if REQUEST and instance.isActiveOrRunning():
            #Actions that require pull and use openflow permissions
            if [r for r in REQUEST.AUTHENTICATED_USER.getRolesInContext(self) if r in workitem.pull_roles]:
                #selfAssignWorkitem
                if workitem.status=='inactive' and workitem.actor=='':
                    actions['Self Assign'] = absolute_url+'/selfAssignWorkitem'+parameters
                #suspendWorkitem
                if workitem.status=='inactive' and workitem.actor==user_name and not workitem.blocked:
                    actions['Suspend'] = absolute_url+'/suspendWorkitem'+parameters
                #resumeWorkitem
                if workitem.status=='suspended' and workitem.actor==user_name:
                    actions['Resume'] = absolute_url+'/resumeWorkitem'+parameters
                #falloutWorkitem
                if (workitem.status=='inactive' or workitem.status=='active') \
                   and workitem.actor==user_name\
                   and not workitem.blocked:
                    actions['Fallout'] = absolute_url+'/falloutWorkitem'+parameters
                #Call Application        getUrlApplicationWithParameters
                if workitem.status in ['inactive','active'] \
                   and activity.kind!='subflow'\
                   and not workitem.blocked:
                    actions['Call Application'] = absolute_url+'/'+self.getApplicationUrlWithParameters(instance_id,workitem_id)
            #Actions that require push and use openflow permissions
            if [r for r in REQUEST.AUTHENTICATED_USER.getRolesInContext(self) if r in workitem.push_roles]:
                #assignWorkitem
                if workitem.status=='inactive' and workitem.actor=='':
                    suppl_parameters = '&process_id=%s&activity_id=%s'%(workitem.process_id, workitem.activity_id)
                    if self.id=='portal_openflow':
                        actions['Assign'] = self.aq_parent.absolute_url()+'/pushWorkitem'+parameters+suppl_parameters
                    else:
                        actions['Assign'] = absolute_url+'/manage_pushWorkitem'+parameters+suppl_parameters
                #unassignWorkitem
                if workitem.status=='inactive' and workitem.actor:
                    actions['Unassign'] = absolute_url+'/unassignWorkitem'+parameters
                #falloutWorkitem
                if workitem.status in ['inactive','active']\
                   and not workitem.blocked:
                    actions['Fallout'] = absolute_url+'/falloutWorkitem'+parameters
                #fallinWorkitem
                if workitem.status=='fallout':
                    if self.id=='portal_openflow':
                        actions['Fallin'] = self.aq_parent.absolute_url()+'/chooseFallin'+parameters
                    else:
                        actions['Fallin'] = absolute_url+'/manage_chooseFallin'+parameters
                #endFallinWorkitem
                if workitem.status=='fallout':
                    actions['End Fallin'] = absolute_url+'/endFallinWorkitem'+parameters
            #Actions that require manage openflow permissions
            if REQUEST.AUTHENTICATED_USER.has_permission('Manage OpenFlow', self):
                #activateWorkitem
                if workitem.status=='inactive' and not workitem.blocked:
                    actions['Activate'] = absolute_url+'/activateWorkitem'+parameters
                #completeWorkitem
                if workitem.status=='active':
                    actions['Complete'] = absolute_url+'/completeWorkitem'+parameters
                #forwardWorkitem
                if workitem.status=='complete' and not workitem.forwarded:
                    actions['Forward'] = absolute_url+'/forwardWorkitem'+parameters
                #inactivateWorkitem
                if workitem.status=='active':
                    actions['Inactive'] = absolute_url+'/inactivateWorkitem'+parameters
            #Actions that require user to be workitem's actor
            if workitem.actor==REQUEST.AUTHENTICATED_USER.getUserName():
                #inactivateWorkitem
                if workitem.status=='active':
                    actions['Inactive'] = absolute_url+'/inactivateWorkitem'+parameters
                #Call Application        getUrlApplicationWithParameters
                if workitem.status in ['inactive','active'] \
                   and activity.kind!='subflow'\
                   and not workitem.blocked:
                    actions['Call Application'] = absolute_url+'/'+self.getApplicationUrlWithParameters(instance_id,workitem_id)

        return actions

    security.declareProtected('Manage OpenFlow', 'getUserActionsOnInstance')
    def getUserActionsOnInstance(self, instance_id, REQUEST=None):
        """ Return the actions that user can do on the instance (filtered on permissions only)"""
        instance = getattr(self, instance_id)
        actions = {}
        absolute_url = self.absolute_url()
        parameters = '?instance_id=%s'%(instance_id)
        if REQUEST:
            if instance.status == 'initiated':
                actions['Activate'] = absolute_url+'/startInstance'+parameters
            if instance.isActiveOrRunning() or instance.status == 'initiated':
                actions['Suspend'] = absolute_url+'/suspendInstance'+parameters
            if instance.status == 'suspended':
                actions['Resume'] = absolute_url+'/resumeInstance'+parameters
            if instance.status=='complete' or instance.status=='terminate':
                actions['Delete'] = absolute_url+"/deleteInstance?inst_ids:list=%s"%(instance_id)
            if instance.status != 'complete':
                actions['Terminate'] = absolute_url+'/terminateInstance'+parameters
        return actions



InitializeClass(CMFOpenflowTool)
