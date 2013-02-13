import ZODB,Globals
import OFS.Application
import unittest
import Zope
from CMFOpenflow.CMFOpenflowTool import CMFOpenflowTool
from CMFOpenflow.instance import instance
from CMFOpenflow.workitem import workitem
from CMFOpenflow.process import process
from CMFOpenflow.activity import activity
from CMFOpenflow.transition import transition

Zope.app().Control_Panel.initialize_cache()

class routingSimpleTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create a Process Definition with two activity (Begin, End) and one transition.
        self.of.addProcess(id='begin_end', BeginEnd=1)
        self.pd = getattr(self.of, 'begin_end')
        self.pd.addTransition(id='begin_end', From='Begin', To='End')
        getattr(self.pd, 'Begin').edit(kind='standard')
        getattr(self.pd, 'End').edit(kind='standard')


        # Create a Process Instance of the Process definition mentioned above
        pid = self.of.addInstance('begin_end', 'test', 'testComment', 'TestTitle', 0)
        self.pi = getattr(self.of, pid)

    def checkCreation(self):
        """ Check for the correct creation of the test objects """
        assert self.of, 'openflow folder not created'
        assert self.pd, 'process definition not created'
        assert getattr(self.pd, 'Begin'), 'Begin activity not created'
        assert getattr(self.pd, 'End'), 'End activity not created'
        assert getattr(self.pd, 'begin_end'), 'begin_end transition not created'
        assert self.pi, 'process instance not created'


    def checkActivateInstance(self):
        """ Check the Process Instance activation """
        assert self.pi.status == 'initiated', 'process instance starting status not correct'
        self.of.startInstance(self.pi.id)
        assert self.pi.status == 'running', 'process instance activation not correct'


    def checkSuspendInstance(self):
        """ Check the Process Instance activation """
        assert self.pi.status == 'initiated', 'process instance starting status not correct'
        self.of.suspendInstance(self.pi.id)
        assert self.pi.status == 'suspended', 'process instance suspension not correct'


    def checkResumeInstance(self):
        """ Check the Process Instance activation """
        assert self.pi.status == 'initiated', 'process instance starting status not correct'
        self.of.suspendInstance(self.pi.id)
        assert self.pi.status == 'suspended', 'process instance suspension not correct'
        self.of.resumeInstance(self.pi.id)
        assert self.pi.status == 'initiated', 'process instance suspension not correct'


    def checkTerminationInstance(self):
        """ Check the Process Instance activation """
        assert self.pi.status == 'initiated', 'process instance starting status not correct'
        self.of.terminateInstance(self.pi.id)
        assert self.pi.status == 'terminated', 'process instance suspension not correct'


    def checkAssignUnassignedWorkitem(self):
        """ Check the workitem creation and activation """
        self.of.startInstance(self.pi.id)
        self.w = getattr(self.pi, '0')
        assert self.w.status == 'inactive', 'workitem creation not correct'
        self.of.assignWorkitem(self.pi.id, self.w.id, 'testActor')
        assert self.w.actor == 'testActor', 'workitem assignement not correct'
        self.of.unassignWorkitem(self.pi.id, self.w.id)
        assert self.w.actor == '', 'workitem unassignement not correct'


    def checkActivateWorkitem(self):
        """ Check the workitem creation and activation """
        self.of.startInstance(self.pi.id)
        self.w = getattr(self.pi, '0')
        assert self.w.status == 'inactive', 'workitem creation not correct'
        self.of.activateWorkitem(self.pi.id, self.w.id)
        assert self.w.status == 'active', 'workitem activation not correct'


    def checkInactivateWorkitem(self):
        """ Check the workitem inactivation """
        self.of.startInstance(self.pi.id)
        self.w = getattr(self.pi, '0')
        assert self.w.status == 'inactive', 'workitem creation not correct'
        self.of.activateWorkitem(self.pi.id, self.w.id)
        assert self.w.status == 'active', 'workitem activation not correct'
        self.of.inactivateWorkitem(self.pi.id, self.w.id)
        assert self.w.status == 'inactive', 'workitem inactivation not correct'


    def checkSuspendWorkitem(self):
        """ Check the workitem suspended """
        self.of.startInstance(self.pi.id)
        self.w = getattr(self.pi, '0')
        assert self.w.status == 'inactive', 'workitem creation not correct'
        self.of.suspendWorkitem(self.pi.id, self.w.id)
        assert self.w.status == 'suspended', 'workitem suspension not correct'


    def checkResumeWorkitem(self):
        """ Check the workitem resume """
        self.of.startInstance(self.pi.id)
        self.w = getattr(self.pi, '0')
        assert self.w.status == 'inactive', 'workitem creation not correct'
        self.of.suspendWorkitem(self.pi.id, self.w.id)
        assert self.w.status == 'suspended', 'workitem suspension not correct'
        self.of.resumeWorkitem(self.pi.id, self.w.id)
        assert self.w.status == 'inactive', 'workitem inactivation not correct'


    def checkCompleteWorkitem(self):
        """ Check the workitem completion """
        self.of.startInstance(self.pi.id)
        self.w = getattr(self.pi, '0')
        self.of.activateWorkitem(self.pi.id, self.w.id)
        self.of.completeWorkitem(self.pi.id, self.w.id)
        assert self.w.status == 'complete', 'workitem completion not correct'


    def checkForwardWorkitem(self):
        """ Check the workitem forwarding """
        self.of.startInstance(self.pi.id)
        self.w0 = getattr(self.pi, '0')
        self.of.activateWorkitem(self.pi.id, self.w0.id)
        self.of.completeWorkitem(self.pi.id, self.w0.id)
        self.of.forwardWorkitem(self.pi.id, self.w0.id)
        assert getattr(self.pi, '1'), 'new workitem not created'
        assert getattr(self.pi, '1').status == 'inactive', 'new workitem status not correct'


    def checkCompleteInstance(self):
        """ Check the process instance completion """
        self.of.startInstance(self.pi.id)
        self.w0 = getattr(self.pi, '0')
        self.of.activateWorkitem(self.pi.id, self.w0.id)
        self.of.completeWorkitem(self.pi.id, self.w0.id)
        self.of.forwardWorkitem(self.pi.id, self.w0.id)
        self.w1 = getattr(self.pi, '1')
        self.of.activateWorkitem(self.pi.id, self.w1.id)
        self.of.completeWorkitem(self.pi.id, self.w1.id)
        assert self.w0.status == 'complete', 'first workitem completion not correct'
        assert self.w1.status == 'complete', 'last workitem completion not correct'
        assert self.pi.status == 'complete', 'process instance completion not correct'


class routingAndSplitTestCase(unittest.TestCase):

    def setUp(self):

        # Create an OpenFlow folder 
        self.of = CMFOpenflowTool('of')
        
        # Create a Process Definition with two parallel activity
        self.of.addProcess(id='begin_end', BeginEnd=1)
        self.pd = getattr(self.of, 'begin_end')
        self.pd.addActivity('a1')
        self.pd.addActivity('a2')
        self.pd.addTransition(id='Begin_a1', From='Begin', To='a1')
        self.pd.addTransition(id='Begin_a2', From='Begin', To='a2')
        self.pd.addTransition(id='a1_End', From='a1', To='End')
        self.pd.addTransition(id='a2_End', From='a2', To='End')
        getattr(self.pd, 'Begin').edit(kind='standard')
        getattr(self.pd, 'End').edit(kind='standard')

        # Create and activate a Process Instance of the Process definition mentioned above
        pid = self.of.addInstance('begin_end', 'test', 'testComment', 'TestTitle', 0)
        self.pi = getattr(self.of, pid)
        self.of.startInstance(self.pi.id)

        # Forward first workitem
        self.w0 = getattr(self.pi, '0')
        self.of.activateWorkitem(self.pi.id, self.w0.id)
        self.of.completeWorkitem(self.pi.id, self.w0.id)
        self.of.forwardWorkitem(self.pi.id, self.w0.id)

    def checkWorkitemSplit(self):
        """ Check the workitem split to two parallel activity"""
        assert getattr(self.pi, '1'), 'workitem 1 not created'
        assert getattr(self.pi, '2'), 'workitem 2 not created'
        assert getattr(self.pi, '1').status == 'inactive', 'workitem 1 status not correct'
        assert getattr(self.pi, '2').status == 'inactive', 'workitem 2 status not correct'


    def checkWorkitemJoin(self):
        """ Check the workitem join from two parallel activity """
        self.w1 = getattr(self.pi, '1')
        self.of.activateWorkitem(self.pi.id, self.w1.id)
        self.of.completeWorkitem(self.pi.id, self.w1.id)
        self.of.forwardWorkitem(self.pi.id, self.w1.id)
        assert getattr(self.pi, '3'), 'workitem 3 not created'
        assert getattr(self.pi, '3').blocked, 'workitem 3 is not blocked'
        self.w2 = getattr(self.pi, '2')
        self.of.activateWorkitem(self.pi.id, self.w2.id)
        self.of.completeWorkitem(self.pi.id, self.w2.id)
        self.of.forwardWorkitem(self.pi.id, self.w2.id)
        assert getattr(self.pi, '3').status == 'inactive', 'workitem 3 is not inactive'
        assert not getattr(self.pi, '3').blocked, 'workitem 3 is still blocked'


class routingXOrSplitTestCase(unittest.TestCase):

    def setUp(self):

        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create a Process Definition with two activity (Begin, End) and one transition.
        self.of.addProcess(id='xor_split', BeginEnd=1)
        self.pd = getattr(self.of, 'xor_split')
        begin = getattr(self.pd, 'Begin')
        begin.edit(split_mode='xor')
        end = getattr(self.pd, 'End')
        end.edit(join_mode='xor')
        self.pd.addActivity('a1')
        self.pd.addActivity('a2')
        self.pd.addTransition(id='Begin_a1', From='Begin', To='a1', condition='python:1')
        self.pd.addTransition(id='Begin_a2', From='Begin', To='a2', condition='python:0')
        self.pd.addTransition(id='a1_End', From='a1', To='End')
        self.pd.addTransition(id='a2_End', From='a2', To='End')
        getattr(self.pd, 'Begin').edit(kind='standard')
        getattr(self.pd, 'End').edit(kind='standard')

        # Create and activate a Process Instance of the Process definition mentioned above
        pid = self.of.addInstance('xor_split', 'test', 'testComment', 'TestTitle', 0)
        self.pi = getattr(self.of, pid)
        self.of.startInstance(self.pi.id)

        # Forward first workitem
        self.w0 = getattr(self.pi, '0')
        self.of.activateWorkitem(self.pi.id, self.w0.id)
        self.of.completeWorkitem(self.pi.id, self.w0.id)
        self.of.forwardWorkitem(self.pi.id, self.w0.id)
 
    def checkWorkitemSplit(self):
        """ Check the workitem split to two alternative activity"""
        assert getattr(self.pi, '1'), 'workitem 1 not created'
        assert getattr(self.pi, '1').activity_id == 'a1', 'workitem 1 activity not correct'
        assert not hasattr(self.pi, '2'), 'workitem 2 created'


    def checkWorkitemJoin(self):
        """ Check the workitem join from two alternative activity"""
        self.w1 = getattr(self.pi, '1')
        self.of.activateWorkitem(self.pi.id, self.w1.id)
        self.of.completeWorkitem(self.pi.id, self.w1.id)
        self.of.forwardWorkitem(self.pi.id, self.w1.id)
        assert getattr(self.pi, '2'), 'workitem 2 not created'
        assert getattr(self.pi, '2').activity_id == 'End', 'activity of workitem 2 is not correct'

        
class routingExceptionHandlingTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder 
        self.of = CMFOpenflowTool('of')
        
        # Create a Process Definition with two activity (Begin, End) and one transition.
        self.of.addProcess(id='exception_handling', BeginEnd=1)
        self.pd = getattr(self.of, 'exception_handling')
        self.pd.addTransition(id='exception_handling', From='Begin', To='End')
        getattr(self.pd, 'Begin').edit(kind='standard')
        getattr(self.pd, 'End').edit(kind='standard')

        # Create a Process Instance of the Process definition mentioned above
        pid = self.of.addInstance('exception_handling', 'test', 'testComment', 'TestTitle', 1)
        self.pi = getattr(self.of, pid)
    

    def checkFallout(self):
        self.of.falloutWorkitem(self.pi.id, '0'), 'fall out not correct'
        assert getattr(self.pi, '0').status == 'fallout', 'first workitem status not correct'
        self.of.fallinWorkitem(self.pi.id, '0', 'exception_handling', 'Begin'), 'fall in not correct'
        self.of.endFallinWorkitem(self.pi.id, '0'), 'fall out not correct'
        assert getattr(self.pi, '0').status != 'fallout', 'first workitem status not correct' 


class routingAutoAppTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')
        
        # Create a Process Definition with two activity (Begin, End) and one transition.
        self.of.addProcess(id='begin_end', BeginEnd=1)
        self.pd = getattr(self.of, 'begin_end')
        self.pd.addTransition(id='begin_end', From='Begin', To='End')
        begin = getattr(self.pd, 'Begin')
        begin.edit(application='testApp',kind='standard', start_mode=1, finish_mode=1)
        getattr(self.pd, 'End').edit(application='testApp',kind='standard')
        # Create a Process Instance of the Process definition mentioned above
        pid = self.of.addInstance('begin_end', 'test', 'testComment', 'TestTitle', 1)
        self.pi = getattr(self.of, pid)

    
    def checkCompleteInstance(self):
        """ Check the process instance completion """
        assert getattr(self.pd, 'Begin').isAutoStart() == 1, 'activity not AutoStart'
        assert getattr(self.pi, '0'), 'first workitem not created'
        assert getattr(self.pi, '0').status == 'complete', 'first workitem not completed'
        self.w1 = getattr(self.pi, '1')
        self.of.activateWorkitem(self.pi.id, self.w1.id)
        self.of.completeWorkitem(self.pi.id, self.w1.id)
        assert self.w1.status == 'complete', 'last workitem completion not correct'
        assert self.pi.status == 'complete', 'process instance completion not correct'

class automaticRoutingSimpleTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create a Process Definition Begin-End
        self.of.addProcess(id='main', BeginEnd=1)
        self.main_pd = getattr(self.of, 'main')
        self.main_pd.addActivity('sub', subflow='test_subflow')
        self.main_pd.addTransition(id='Begin_End', From='Begin', To='End')
        getattr(self.main_pd, 'Begin').edit(kind='dummy')
        getattr(self.main_pd, 'End').edit(kind='dummy')

        # Create a Process Instance of "main"
        pid = self.of.addInstance('main', 'test', 'testComment', 'TestTitle')
        self.pi = getattr(self.of, pid)


    def checkCorrectCompletion(self):
        """ Check the simple process workitems completion """
        self.of.startInstance(self.pi.id)
        assert getattr(self.pi, '0'), 'workitem 0 (Begin)  not created'
        assert getattr(self.pi, '1'), 'workitem 1  (End) not created'
        assert getattr(self.pi, '0').status=='complete', 'workitem 0 (Begin)  not completed'
        assert getattr(self.pi, '1').status=='complete', 'workitem 1 (End)  not completed'


class routingSubflowTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create a Process Definition with a subflow activity.
        self.of.addProcess(id='main', BeginEnd=1)
        self.main_pd = getattr(self.of, 'main')
        self.main_pd.addActivity('sub', kind='subflow', subflow='test_subflow')
        self.main_pd.addTransition(id='Begin_sub', From='Begin', To='sub')
        self.main_pd.addTransition(id='sub_End', From='sub', To='End')
        begin = getattr(self.main_pd, 'Begin')
        begin.edit(start_mode=1, finish_mode=1)

        # Create a Process Definition "subflow" that will act as a subflow.
        self.of.addProcess(id='test_subflow', BeginEnd=1)
        self.sub_pd = getattr(self.of, 'test_subflow')
        self.sub_pd.addTransition(id='Begin_End', From='Begin', To='End')
        getattr(self.sub_pd, 'Begin').edit(kind='standard')
        getattr(self.sub_pd, 'End').edit(kind='standard')

        # Create a Process Instance of "main"
        pid = self.of.addInstance('main', 'test', 'testComment', 'TestTitle', 1)
        self.pi = getattr(self.of, pid)


    def checkSubflowWorkitemsCreation(self):
        """ Check the subflow workitems creation """
        assert getattr(self.pi, '1'), 'workitem 1  not created'
        assert getattr(self.pi, '2').activity_id == 'Begin' , 'workitem 2 activity not correct'
        assert getattr(self.pi, '2').process_id == 'test_subflow' , 'workitem 2 process not correct'
        self.w = getattr(self.pi, '2')
        self.of.activateWorkitem(self.pi.id, self.w.id)
        self.of.completeWorkitem(self.pi.id, self.w.id)
        self.of.forwardWorkitem(self.pi.id, self.w.id)
        assert getattr(self.pi, '3').activity_id == 'End' , 'workitem 3 activity not correct'
        assert getattr(self.pi, '3').process_id == 'test_subflow' , 'workitem 3 process not correct'


    def checkCompleteSubflow(self):
        """ Check the subflow completion """
        self.w = getattr(self.pi, '2')
        self.of.activateWorkitem(self.pi.id, self.w.id)
        self.of.completeWorkitem(self.pi.id, self.w.id)
        self.of.forwardWorkitem(self.pi.id, self.w.id)
        assert getattr(self.pi, '3'), 'workitem 3  not created'
        assert self.of.getSubflowWorkitem(self.pi.id, '3',getattr(self.pi, '3').process_id) == '1', 'subflow workitem not correct'
        self.of.activateWorkitem(self.pi.id, '3')
        self.of.completeWorkitem(self.pi.id, '3')
        assert getattr(self.pi, '1').status == 'complete', 'subflow workitem status not correct'
        assert getattr(self.pi, '4'), 'workitem 4 not created'


class automaticRoutingSubflowTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create a Process Definition with a subflow activity.
        self.of.addProcess(id='main', BeginEnd=1)
        self.main_pd = getattr(self.of, 'main')
        self.main_pd.addActivity('sub', kind='subflow', subflow='test_subflow')
        self.main_pd.addTransition(id='Begin_sub', From='Begin', To='sub')
        self.main_pd.addTransition(id='sub_End', From='sub', To='End')
        getattr(self.main_pd, 'Begin').edit(kind='dummy')
        getattr(self.main_pd, 'End').edit(kind='dummy')

        # Create a Process Definition "subflow" that will act as a subflow with End dummy (automatic finish).
        self.of.addProcess(id='test_subflow', BeginEnd=1)
        self.sub_pd = getattr(self.of, 'test_subflow')
        self.sub_pd.addTransition(id='Begin_End', From='Begin', To='End')
        getattr(self.sub_pd, 'Begin').edit(kind='dummy')
        getattr(self.sub_pd, 'End').edit(kind='dummy')

        # Create a Process Instance of "main"
        pid = self.of.addInstance('main', 'test', 'testComment', 'TestTitle', 1)
        self.pi = getattr(self.of, pid)


    def checkRouting(self):
        """ Check the workitems creation and correct completion of a subflow"""
        assert getattr(self.pi, '1'), 'workitem 1  not created'
        assert getattr(self.pi, '2').activity_id == 'Begin' , 'workitem 2 activity not correct'
        assert getattr(self.pi, '2').process_id == 'test_subflow' , 'workitem 2 process not correct'
        self.w = getattr(self.pi, '2')
        assert getattr(self.pi, '1').status == 'complete' , 'workitem 1 not complete'
        assert getattr(self.pi, '3').activity_id == 'End' , 'workitem 3 activity not correct'
        assert getattr(self.pi, '3').process_id == 'test_subflow' , 'workitem 3 process not correct'
        assert getattr(self.pi, '3').status == 'complete' , 'workitem 3 not complete'
        assert getattr(self.pi, '4').activity_id == 'End' , 'workitem 4 activity not correct'
        assert getattr(self.pi, '4').process_id == 'main' , 'workitem 4 process not correct'
        assert getattr(self.pi, '4').status == 'complete' , 'workitem 4 not complete'

    def checkReports(self):
      """ Check Reports """
      checkReports(self)


class catalogTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create a Process Definition with two activity (Begin, End) and one transition.
        self.of.addProcess(id='begin_end', BeginEnd=1)
        self.pd = getattr(self.of, 'begin_end')
        self.pd.addTransition(id='begin_end', From='Begin', To='End')

        # Create a Process Instance of the Process definition mentioned above
        pid = self.of.addInstance('begin_end', 'test', 'testComment', 'TestTitle', 0)
        self.pi = getattr(self.of, pid)


    def checkCatalogCreation(self):
        assert hasattr(self.of, 'Catalog'), 'Catalog not created'


    def checkProcessCataloging(self):
        catalog = getattr(self.of, 'Catalog')
        assert catalog.searchResults({'id': 'begin_end'}), 'Process not Cataloged'

class countWorkitemsTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create some Process Definition
        for id in ['first','second','third']:
            self.of.addProcess(id=id, BeginEnd=1)
            self.pd = getattr(self.of, id)
            self.pd.addTransition(id=id, From='Begin', To='End')
            self.pd['Begin'].edit(kind='Standard')
            # Routing: 6 workitems
            # instance with workitem inactive and unassigned
            pid = self.of.addInstance(id, 'test1', 'testComment', 'TestTitle', 1)
            # instance with workitem inactive and assigned
            pid = self.of.addInstance(id, 'test2', 'testComment', 'TestTitle', 1)
            pid = self.of.assignWorkitem(pid,'0','testUser')
            # instance with workitem active
            pid = self.of.addInstance(id, 'test3', 'testComment', 'TestTitle', 1)
            self.of.activateWorkitem(pid,'0','testUser')
            # instance with workitem completed
            pid=self.of.addInstance(id, 'test4', 'testComment', 'TestTitle', 1)
            self.of.activateWorkitem(pid,'0','testUser')
            self.of.completeWorkitem(pid,'0')
            # instance with 2 workitems completed
            pid=self.of.addInstance(id, 'test5', 'testComment', 'TestTitle', 1)
            self.of.activateWorkitem(pid,'0','testUser')
            self.of.completeWorkitem(pid,'0')
            self.of.forwardWorkitem(pid,'0')

    def checkCountWorkitems(self):
        """ Check results of countWorkitems"""
        assert self.of.countWorkitems()=={'to do':'6', 'to assign':'3', 'completed':'9'},'Result error for process'
        assert self.of.countWorkitems('first')=={'to do':'2', 'to assign':'1', 'completed':'3'},'Result error for process'
        assert self.of.countWorkitems('first','Begin')=={'to do':'2', 'to assign':'1', 'completed':'2'},'Result error for process and activity'
        assert self.of.countWorkitems('first','Begin','testUser')=={'to do':'2', 'to assign':'1', 'completed':'2'},'Result error for process, activity and user'

class iteractionSubflowTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create base Process Definition
        self.of.addProcess(id='main', BeginEnd=1)
        self.main_pd = getattr(self.of, 'main')
        self.main_pd.addActivity('subProcess', kind='subflow', subflow='iteraction_subflow')
        self.main_pd.addTransition(id='Begin_subProcess', From='Begin', To='subProcess')
        self.main_pd.addTransition(id='subProcess_End', From='subProcess', To='End')
        getattr(self.main_pd, 'Begin').edit(kind='dummy')
        getattr(self.main_pd, 'End').edit(kind='dummy')

        # Create iteraction Process Definition
        self.of.addProcess(id='iteraction_subflow', BeginEnd=1)
        self.sub_pd = getattr(self.of, 'iteraction_subflow')
        self.sub_pd.addActivity('subCall', kind='subflow', subflow='iteraction_subflow')
        self.sub_pd.addTransition(id='Begin_subCall', From='Begin',
                To='subCall', condition='python:here.sub')
        self.sub_pd.addTransition(id='Begin_End', From='Begin',
                To='End', condition='python:not here.sub')
        self.sub_pd.addTransition(id='subCall_End', From='subCall',To='End')
        getattr(self.sub_pd, 'Begin').edit(kind='standard', split_mode='xor', finish_mode=1)
        getattr(self.sub_pd, 'End').edit(kind='dummy', join_mode='xor')

        # Create a Process Instance of "main"
        pid = self.of.addInstance('main', 'test', 'testComment', 'TestTitle', 1)
        self.pi = getattr(self.of, pid)


    def checkRouting(self):
        """ create a routing to subflow and complete """
        w = getattr(self.pi, '2')
        assert w.activity_id=='Begin' and w.process_id=='iteraction_subflow', 'no begin in subflow'
        self.of.activateWorkitem(self.pi.id, w.id)
        self.pi.sub=1 # entry in sub-subflow
        self.of.completeWorkitem(self.pi.id, w.id)

        w = getattr(self.pi, '4')
        assert w.activity_id=='Begin' and w.process_id=='iteraction_subflow', 'no begin in subflow-2'
        self.of.activateWorkitem(self.pi.id, w.id)
        self.pi.sub=0 # exit from subflow
        self.of.completeWorkitem(self.pi.id, w.id)

        w = getattr(self.pi, '7')
        assert w.activity_id=='End' and w.process_id=='main', 'no End'

    def checkReports(self):
      """ Check Reports """
      checkReports(self)

class recursiveSubflowTestCase(unittest.TestCase):

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create base Process Definition
        self.of.addProcess(id='main', BeginEnd=1)
        self.main_pd = getattr(self.of, 'main')
        self.main_pd.addActivity('subProcess', kind='subflow', subflow='main')
        self.main_pd.addTransition(id='Begin_subProcess',
                                   From='Begin',
                                   To='subProcess',
                                   condition='python:here.sub')
        self.main_pd.addTransition(id='Begin_End',
                                   From='Begin',
                                   To='End',
                                   condition='python:not here.sub')
        self.main_pd.addTransition(id='subProcess_End',
                                   From='subProcess',
                                   To='End')

        getattr(self.main_pd, 'Begin').edit(kind='standard', split_mode='xor', finish_mode=1)
        getattr(self.main_pd, 'End').edit(kind='dummy', join_mode='xor')

        # Create a Process Instance of "main"
        pid = self.of.addInstance('main', 'test', 'testComment', 'TestTitle', 1)
        self.pi = getattr(self.of, pid)

    def checkRouting(self):
        """ create a routing to subflow and complete """
        self.pi.sub = 1
        w = getattr(self.pi, '0')
        self.of.activateWorkitem(self.pi.id, w.id)
        self.of.completeWorkitem(self.pi.id, w.id)
        w = getattr(self.pi, '2')
        assert w.activity_id=='Begin', 'First recursion nok'

        self.of.activateWorkitem(self.pi.id, w.id)
        try:
          self.of.completeWorkitem(self.pi.id, w.id)
        except:
          # self.pi.getJoiningWorkitem('main', 'Begin', '5')==[]
          assert 0, 'Incorrect joining workitem'
        w = getattr(self.pi, '4')
        assert w.activity_id=='Begin', 'Second recursion nok'

        self.pi.sub = 0
        self.of.activateWorkitem(self.pi.id, w.id)
        self.of.completeWorkitem(self.pi.id, w.id)
        w = getattr(self.pi, '5')
        assert w.activity_id=='End', 'Completion nok'

    def checkReports(self):
      """ Check Reports """
      checkReports(self)

def checkReports(self):
    """ Check Reports """
    self.checkRouting()
    tot = 0
    for event in self.pi.initiation_log:
      tot += event['end']-event['start']
    assert tot==self.pi.initiation_time
    tot = 0
    for event in self.pi.running_log:
      tot += event['end']-event['start']
    assert tot==self.pi.running_time
    tot = 0
    for event in self.pi.activation_log:
      tot += event['end']-event['start']
    assert tot==self.pi.active_time

class routingAndSubflowsTestCase(unittest.TestCase):
    """ Test routing of two parallel subflow activities """

    def setUp(self):
        # Create an OpenFlow folder
        self.of = CMFOpenflowTool('of')

        # Create a Process Definition with a subflow activity.
        self.of.addProcess(id='main', BeginEnd=1)
        self.main_pd = getattr(self.of, 'main')
        self.main_pd.addActivity('sub1', kind='subflow', subflow='test_subflow')
        self.main_pd.addActivity('sub2', kind='subflow', subflow='test_subflow')
        self.main_pd.addTransition(id='Begin_sub1', From='Begin', To='sub1')
        self.main_pd.addTransition(id='Begin_sub2', From='Begin', To='sub2')
        self.main_pd.addTransition(id='sub1_End', From='sub1', To='End')
        self.main_pd.addTransition(id='sub2_End', From='sub2', To='End')
        getattr(self.main_pd, 'Begin').edit(kind='dummy')
        getattr(self.main_pd, 'End').edit(kind='dummy')

        # Create a Process Definition "subflow" that will act as a subflow with End dummy (automatic finish).
        self.of.addProcess(id='test_subflow', BeginEnd=1)
        self.sub_pd = getattr(self.of, 'test_subflow')
        self.sub_pd.addTransition(id='Begin_End', From='Begin', To='End')
        getattr(self.sub_pd, 'Begin').edit(kind='dummy')
        getattr(self.sub_pd, 'End').edit(kind='dummy')

        # Create a Process Instance of "main"
        pid = self.of.addInstance('main', 'test', 'testComment', 'TestTitle', 1)
        self.pi = getattr(self.of, pid)


    def checkRouting(self):
        """ Check the routing of two parallel subflow activities """
        assert getattr(self.pi, '0'), 'workitem 0  not created'
        assert getattr(self.pi, '1').activity_id == 'sub1' , 'workitem 1 activity not correct'
        assert getattr(self.pi, '1').process_id == 'main' , 'workitem 1 process not correct'
        assert getattr(self.pi, '2').activity_id == 'sub2' , 'workitem 2 activity not correct'
        assert getattr(self.pi, '2').process_id == 'main' , 'workitem 2 process not correct'
        assert getattr(self.pi, '4').activity_id == 'End' , 'workitem 4 activity not correct'
        assert getattr(self.pi, '4').process_id == 'test_subflow' , 'workitem 4 process not correct'
        assert getattr(self.pi, '4').status == 'complete' , 'workitem 4 not complete'
        assert getattr(self.pi, '7').activity_id == 'End' , 'workitem 6 activity not correct'
        assert getattr(self.pi, '7').process_id == 'test_subflow' , 'workitem 6 process not correct'
        assert getattr(self.pi, '7').status == 'complete' , 'workitem 6 not complete'
        assert getattr(self.pi, '5').activity_id == 'End' , 'workitem 5 activity not correct'
        assert getattr(self.pi, '5').process_id == 'main' , 'workitem 5 process not correct'
        assert getattr(self.pi, '5').status == 'complete' , 'workitem 5 not complete'

    def checkReports(self):
      """ Check Reports -> remove? """
      checkReports(self)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = unittest.makeSuite(routingSimpleTestCase, 'check')

    suite.addTest(unittest.makeSuite(routingAndSubflowsTestCase, 'check'))
    suite.addTest(unittest.makeSuite(recursiveSubflowTestCase, 'check'))
    suite.addTest(unittest.makeSuite(iteractionSubflowTestCase, 'check'))
    suite.addTest(unittest.makeSuite(routingAndSplitTestCase, 'check'))
    suite.addTest(unittest.makeSuite(routingXOrSplitTestCase, 'check'))
    suite.addTest(unittest.makeSuite(routingExceptionHandlingTestCase, 'check'))
    suite.addTest(unittest.makeSuite(routingAutoAppTestCase, 'check'))
    suite.addTest(unittest.makeSuite(automaticRoutingSimpleTestCase, 'check'))
    suite.addTest(unittest.makeSuite(routingSubflowTestCase, 'check'))
    suite.addTest(unittest.makeSuite(automaticRoutingSubflowTestCase, 'check'))
    suite.addTest(unittest.makeSuite(catalogTestCase, 'check'))
    suite.addTest(unittest.makeSuite(countWorkitemsTestCase, 'check'))

    runner.run(suite)
