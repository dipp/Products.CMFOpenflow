import ZODB, Globals, OFS.Application
import unittest
import Zope
from CMFOpenflow.activity import activity



class activityTestCase(unittest.TestCase):


    def setUp(self):

        # Create an Activity
        self.activity = activity('testActivity','testProcess')
        assert self.activity, 'activity not created'


    def checkManageActivityPushRoles(self):
        """ Check edit and get of push roles list """
        self.activity.editPushRoles(['testRole'])
        assert 'testRole' in self.activity._push_roles, 'editPushRoles not correct'
        assert 'testRole' in self.activity.getPushRoles(), 'getPushRoles no correct'
        
    def checkManageActivityPullRoles(self):
        """ Check edit and get of pull roles list """
        self.activity.editPullRoles(['testRole'])
        assert 'testRole' in self.activity._pull_roles, 'editPullRoles not correct'
        assert 'testRole' in self.activity.getPullRoles(), 'getPullRoles no correct'


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = unittest.makeSuite(activityTestCase, 'check')
    runner.run(suite)
