from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from time import time
from OFS.SimpleItem import SimpleItem 
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware
from zLOG import LOG, ERROR

class workitem(CatalogPathAware, SimpleItem):
    """ describes a single workitem of the history graph """

    def __init__(self, id, instance_id, process_id, activity_id, blocked,
                 priority=0, workitems_from=[], workitems_to=[],
                 push_roles=[], pull_roles=[], title='') :
        self.id = id
        self.title = title
        self.activity_id = activity_id
        self.process_id = process_id
        self.instance_id = instance_id
        self.workitems_from = workitems_from[:]
        self.workitems_to = workitems_to[:]
        self.status = 'inactive'
        #possible states: inactive,active,suspended,fallout,complete
        self.event_log = []
        self.actor = ''
        self.graph_level = 0
        self.priority = priority
        self.blocked = blocked
        self.forwarded = 0
        self.push_roles = push_roles
        self.pull_roles = pull_roles
        #logging structure
        #each event has the form {'start':xxx, 'end':yyy, 'comment':zzz, 'actor':aaa}
        #'start' and 'end' are time in msec, 'actor' and 'comment' are string
        self.inactivation_log = []
        self.activation_log = []
        self.completion_log = []
        self.suspension_log = []
        self.fallout_log = []
        #statistic data in msec
        self.inactive_time = 0
        self.active_time = 0
        self.suspended_time = 0
        self.fallout_time = 0
        #log initialization
        self.inactivation_log.append({'start':time(),'end':None,'comment':'creation','actor':''})


    meta_type = 'Workitem'


    security = ClassSecurityInfo()


    security.declareProtected('Manage OpenFlow', 'edit')
    def edit(self,
             instance_id = None,
             process_id = None,
             activity_id = None,
             blocked = None,
             priority = None,
             workitems_from = None,
             workitems_to = None,
             status = None,
             actor = None,
             graph_level = None,
             title = None):
        """  """
        if instance_id:
            self.instance_id = instance_id
        if process_id:
            self.process_id = process_id
        if activity_id:
            self.activity_id = activity_id
        if blocked:
            self.blocked = blocked
        if priority:
            self.priority = priority
        if workitems_from:
            self.workitems_from = workitems_from[:]
        if workitems_to:
            self.workitems_to = workitems_to[:]
        if status:
            self.status = status
        if actor:
            self.actor = actor
        if graph_level:
            self.graph_level = graph_level
        if title:
            self.title = title
        self.reindex_object()


    def addFrom(self, id):
        self.workitems_from.append(id)
        self._p_changed=1
        self.reindex_object()


    def addTo(self, id_list):
        self.workitems_to.extend(id_list)
        self._p_changed=1
        self.reindex_object()


    def setBlocked(self, blocked):
        self.blocked = blocked
        # FIX-ME raise an exception
        if self.blocked < 0:
            self.blocked = 0
        self.reindex_object()


    def setPriority(self, priority):
        self.priority = priority
        self.reindex_object()


    def setGraphLevel(self, graph_level):
        self.graph_level = graph_level
        self.reindex_object()


    def addEvent(self, event, comment=''):
        self.event_log.append({'event' : event, 'time' : DateTime(), 'comment': comment})
        self._p_changed=1


    def isActiveOrInactiveOn(self, process_id, activity_id):
        return (self.status in ('active', 'inactive')) \
               and self.process_id == process_id \
               and self.activity_id == activity_id


    def unblock(self, value=1):
        self.blocked = self.blocked - value
        # FIX-ME raise an exception
        if self.blocked < 0:
            self.blocked = 0


    def setStatus(self, status, comment='', actor=''):
        old_status = self.status
        new_status = status
        now = time()

        if old_status == new_status:
            raise "WorkitemActionError","Try to set the same status"

        if old_status == 'inactive':
            self.inactivation_log[-1]['end'] = now
            self.inactive_time += now - self.inactivation_log[-1]['start']
            if new_status == 'active':
                self.activation_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'suspended':
                self.suspension_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'fallout':
                self.fallout_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            else:
                raise "WorkitemActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        if old_status == 'active':
            self.activation_log[-1]['end'] = now
            self.active_time += now - self.activation_log[-1]['start']
            if new_status == 'inactive':
                self.inactivation_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'complete':
                self.completion_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            elif new_status == 'fallout':
                self.fallout_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            else:
                raise "WorkitemActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        if old_status == 'fallout':
            self.fallout_log[-1]['end'] = now
            self.fallout_time += now - self.fallout_log[-1]['start']
            if new_status == 'complete':
                self.completion_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            else:
                raise "WorkitemActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        if old_status == 'suspended':
            self.suspension_log[-1]['end'] = now
            self.suspended_time += now - self.suspension_log[-1]['start']
            if new_status == 'inactive':
                self.inactivation_log.append({'start':now,'end':None,'comment':comment,'actor':actor})
            else:
                raise "WorkitemActionError","Wrong status transition from %s to %s"%(old_status,new_status)

        self.status = status
        self.addEvent(status, comment)

        self.reindex_object()


    def endFallin(self):
        self.setStatus('complete')
        self.forwarded=1
        self.reindex_object()


    def setArrivalTime(self, activity_id, comment):
        self.addEvent("arrival:" + activity_id)
        self.reindex_object()


    def assignTo(self, actor, by=None, comment=''):
        self.actor = actor
        self.addEvent("assigned to " + actor, comment)
        self.reindex_object()

    def getEventLog(self):
        return self.event_log
