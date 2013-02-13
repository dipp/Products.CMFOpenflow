import ZODB, Globals, OFS.Application
import unittest
import Zope


class workitemTestCase(unittest.TestCase):

    def setUp(self):
        from CMFOpenflow.workitem import workitem
        self.w = workitem('id', 'instance_id', 'process_id', 'activity_id', 0, 0)
        
    
    def checkCreation(self):
        """ Check for the correct creation of a workitem """
        assert self.w, 'workitem not created'


    def checkUnblock(self):
        """ Check unblock attribute consistency with unusual values """
        self.w.unblock()
        assert self.w.blocked >= 0, 'uncorrect values for blocked attribute'


    def checkIsActive(self):
        """ we have big problems here """
        pass


    def checkEdit(self):
        """ Check the names of the set methods """
        assert self.w.edit(instance_id = '',
                           process_id = '',
                           activity_id = '',
                           blocked = 0,
                           priority = 1,
                           workitems_from = [],
                           workitems_to = [],
                           status = 'active',
                           actor = 'openflow_test',
                           graph_level = 0) == None, 'uncorrect edit'
        
    

if __name__ == '__main__':
    suite= unittest.makeSuite(workitemTestCase, 'check')
    runner = unittest.TextTestRunner()
    runner.run(suite)
