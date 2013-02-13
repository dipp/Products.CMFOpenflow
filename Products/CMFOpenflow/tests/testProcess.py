import ZODB, Globals, OFS.Application
import unittest
import Zope
from CMFOpenflow.process import process
from CMFOpenflow.activity import activity
from CMFOpenflow.transition import transition


class processDefinitionCreationTestCase(unittest.TestCase):


    def setUp(self):

        # Create a Process Definition with two activity (Begin, End) and one transition
        self.pd = process('begin_end')

    
    def checkProcessInstanceCreation(self):
        """ Check a simple process definition creation """
        self.pd.addActivity('Begin')
        assert getattr(self.pd, 'Begin'), 'Begin activity not created'
        self.pd.addActivity('Act')
        self.pd.addActivity('End')
        self.pd.edit(begin='Begin')
        self.pd.addTransition(id='begin_act', From='Begin', To='Act')
        assert getattr(self.pd, 'begin_act'), 'begin_act transition not created'
        self.pd.addTransition(id='act_end', From='Act', To='End')
        assert getattr(self.pd, 'act_end'), 'act_end transition not created'


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = unittest.makeSuite(processDefinitionCreationTestCase, 'check')
    runner.run(suite)
