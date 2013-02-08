import ZODB, Globals, OFS.Application
import unittest
import Zope


class instanceTestCase(unittest.TestCase):

    def setUp(self):
        from CMFOpenflow.instance import instance
        self.i = instance('id', 'activity_id', 'testsuite', 'TestComment', 'TestTitle')


    def checkCreation(self):
        """ Check for the correct creation of a workitem """
        assert self.i, 'instance not created'


    def checkWorkitemAdd(self):
        """ Check the workitem creation """
        self.i.addWorkitem('process_id', 'activity_id', 0)
        assert self.i.objectValues('Workitem'), 'workitem not created'

    def checkStatusTransitions(self):
        """ Check the possible transitions """
        assert self.i.status=='initiated', "Incorrect status"
        self.i.setStatus('suspended')
        assert self.i.status=='suspended', "Incorrect status"
        self.i.setStatus('initiated')
        assert self.i.status=='initiated', "Incorrect status"
        self.i.setStatus('running')
        assert self.i.status=='running', "Incorrect status"
        self.i.setStatus('suspended')
        assert self.i.status=='suspended', "Incorrect status"
        self.i.setStatus('running')
        assert self.i.status=='running', "Incorrect status"
        self.i.setStatus('active')
        assert self.i.status=='active', "Incorrect status"
        self.i.setStatus('suspended')
        assert self.i.status=='suspended', "Incorrect status"
        self.i.setStatus('active')
        assert self.i.status=='active', "Incorrect status"
        self.i.setStatus('running')
        assert self.i.status=='running', "Incorrect status"
        self.i.setStatus('complete')
        assert self.i.status=='complete', "Incorrect status"

    def checkReport(self):
        """ Check the report logs """
        self.checkStatusTransitions()
        tot = 0
        for event in self.i.initiation_log:
          tot += event['end']-event['start']
        assert tot==self.i.initiation_time
        tot = 0
        for event in self.i.running_log:
          tot += event['end']-event['start']
        assert tot==self.i.running_time
        tot = 0
        for event in self.i.activation_log:
          tot += event['end']-event['start']
        assert tot==self.i.active_time


if __name__ == '__main__':
    suite= unittest.makeSuite(instanceTestCase, 'check')
    runner = unittest.TextTestRunner()
    runner.run(suite)
