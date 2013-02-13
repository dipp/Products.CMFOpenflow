from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from OFS.Folder import Folder
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware
from time import time
from DateTime import DateTime
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from workitem import workitem
from zLOG import LOG, ERROR, INFO


def manage_addInstance(self,
                       process_id,
                       customer,
                       comments,
                       title,
                       activation=0,
                       priority=0,
                       REQUEST=None):
    """ adds an a process definition instance """
    begin_activity_id = getattr(self, process_id).begin
    i = instance(process_id, begin_activity_id, customer, title, comments, priority)
    self._setObject(i.id, i)
    if activation:
        self.startInstance(i.id)
    return i.id


manage_addInstanceForm = PageTemplateFile('zpt/openflow/manage_addInstanceForm', globals())


class instance(CatalogPathAware, Folder):
    """ Even though it is called instance it is more than that: it is the collection
    of all instances related to a given process instance."""


    def __init__(self, process_id, activity_id, customer, title='', comments='', priority=0):
        self.process_id = process_id
        self.customer = customer
        self.comments = comments
        self.id = customer + str(DateTime().timeTime())
        self.creation_time = DateTime()
        self.title = title
        self.priority = priority
        self.begin_process_id = process_id
        self.begin_activity_id = activity_id
        self.status = 'initiated' #Possible states: initiated,running,active,complete,suspended,terminated
        self.old_status = '' #Used to remeber the status after a suspension
        #logging structure
        #each event has the form {'start':xxx, 'end':yyy, 'comment':zzz, 'actor':aaa}
        #'start' and 'end' are time in msec, 'actor' and 'comment' are string
        self.initiation_log = [] #1 log
        self.running_log = []
        self.activation_log = []
        self.completion_log = [] #1 log
        self.suspension_log = []
        self.termination_log = [] #1 log
        #statistic data in msec
        self.initiation_time = 0
        self.running_time = 0
        self.active_time = 0
        self.suspended_time = 0
        #log initialization
        self.initiation_log.append({'start':time(),'end':None,'comment':'creation','actor':''})
        LOG('Instance:',INFO,'Add Instance '+str(self.id))


    security = ClassSecurityInfo()


    security.declareProtected('Use OpenFlow', 'index_html')
    index_html = PageTemplateFile('zpt/instance/History', globals())


    meta_type = 'Instance'


    manage_options = ({'label': 'History', 'action' : 'index_html'}, ) + Folder.manage_options[0:1] + Folder.manage_options[2:]


    def addWorkitem(self, process_id, activity_id, blocked, push_roles=[], pull_roles=[]):
        w_id = str(len(self.objectValues('Workitem')))
        if hasattr(self,'aq_parent'):
            activity = getattr(getattr(self.aq_parent,process_id),activity_id)
            title = activity.title
        else:
            title = ''
        LOG('Openflow', INFO, '%s : %s %s' % ('instance.addWorkitem', self.id, w_id))
        w = workitem(w_id, self.id, process_id, activity_id, blocked,
                     push_roles=push_roles,
                     pull_roles=pull_roles,
                     title=title)
        self._setObject(str(w.id), w)
        w.addEvent('creation')
        return w


    def getJoiningWorkitem(self, workitem_from_id, of):
        w_list = []
        for w in self.objectValues('Workitem'):
          if self[workitem_from_id].activity_id in \
            [t.From for t in of[w.process_id].objectValues('Transition') if w.activity_id==t.To and w.blocked]:
            w_list.append(w)
        if w_list:
              return w_list[0]
        else:
              return None


    def setStatus(self, status, comment='', actor=''):
        old_status = self.status
        new_status = status
        now = time()

        if old_status==new_status:
          raise "InstanceActionError","Try to set the same status"

        if old_status == 'initiated':
            self.initiation_log[-1]['end'] = now
            self.initiation_time += now - self.initiation_log[-1]['start']
            if new_status == 'running':
                self.running_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'suspended':
                self.suspension_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'terminated':
                self.termination_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            else:
              raise "InstanceActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        if old_status == 'running':
            self.running_log[-1]['end'] = now
            self.running_time += now - self.running_log[-1]['start']
            if new_status == 'active':
                self.activation_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'complete':
                self.completion_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'suspended':
                self.suspension_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'terminated':
                self.termination_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            else:
              raise "InstanceActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        if old_status == 'active':
            self.activation_log[-1]['end'] = now
            self.active_time += now - self.activation_log[-1]['start']
            if new_status == 'running':
                self.running_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'suspended':
                self.suspension_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'terminated':
                self.termination_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            else:
              raise "InstanceActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        if old_status == 'suspended':
            self.suspension_log[-1]['end'] = now
            self.suspended_time += now - self.suspension_log[-1]['start']
            if new_status == 'initiated':
              self.initiation_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'running':
                self.running_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'active':
                self.activation_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'complete':
                self.completion_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'terminated':
                self.termination_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            else:
              raise "InstanceActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        if old_status == 'complete':
            self.completion_log[-1]['end'] = now
            self.completion_time += now - self.completion_log[-1]['start']
            if new_status == 'initiated':
              self.initiation_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
              LOG('Instance:',INFO,'Re-initialization Instance '+str(self.id))
            else:
              raise "InstanceActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        if old_status == 'terminated':
          raise "InstanceActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        self.status = status
        self.reindex_object()

    security.declareProtected('Use OpenFlow', 'getActiveWorkitems')
    def getActiveWorkitems(self):
        """ returns the number of active workitems (not of kind 'subflow')"""
        from Acquisition import aq_parent
        w_list=[]
        for w in filter(lambda x: x.status == 'active', self.objectValues('Workitem')):
          activity = aq_parent(self)[w.process_id][w.activity_id]
          if activity.kind!='subflow':
            w_list.append(w)
        return len(w_list)


    def setPriority(self, value):
        self.priority = value
        self.reindex_object()

    def isActiveOrRunning(self):
        return self.status in ('active', 'running')


InitializeClass(instance)
