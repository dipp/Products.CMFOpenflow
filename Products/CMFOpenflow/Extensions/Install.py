from Products.CMFCore.TypesTool import FactoryTypeInformation 
from Products.CMFCore.utils import getToolByName
from Products.CMFOpenflow import CMFOpenflowTool, cmfopenflow_globals
from Products.CMFCore.DirectoryView import addDirectoryViews
from cStringIO import StringIO
import string

def install( self ):
    """ Setup CMFOpenflow """
    msg = ""
    try:
        openflow_id = 'portal_openflow'
        if self.objectValues('CMF OpenFlow Tool'):
            msg += "Delete old portal_openflow..."
            self.manage_delObjects(openflow_id)
            msg += "Done\n"
        msg += "Add new portal_openflow..."
        self.manage_addProduct['CMFOpenflow'].manage_addOpenflow(openflow_id)
        msg += "Done\n"

        portal_actions = getToolByName( self, 'portal_actions')
        if 'worklist' in [action.id for action in portal_actions.listActions()]:
            msg += "Delete old action worklist to portal..."
            listA = portal_actions.listActions()
            selections = tuple([i for i in range(0,len(listA)) if listA[i].id=='worklist'])
            portal_actions.deleteActions(selections)
            msg += "Done\n"
        msg += "Add new action worklist to portal..."
        portal_actions.addAction(
                    id='worklist',
                    name='Worklist',
                    action='string: ${portal_url}/worklist',
                    condition='',
                    permission='Use OpenFlow',
                    category='global',
                    visible=1)
        msg += "Done\n"

        skinstool = getToolByName( self, 'portal_skins' )
        msg += "Add Skins..."
        if 'zpt_cmfopenflow' not in skinstool.objectIds():
            addDirectoryViews( skinstool, 'skins', cmfopenflow_globals)
            #addDirectoryViews( skinstool, 'skins')
            msg += "---"
        skins = skinstool.getSkinSelections()
        for skin in skins:
            path = skinstool.getSkinPath( skin )
            path = map( string.strip, string.split(path, ',') )
            if 'zpt_cmfopenflow' not in path:
                try:
                    path.insert( path.index('content'), 'zpt_cmfopenflow' )
                except ValueError:
                    path.append( 'zpt_cmfopenflow' )
                path = string.join( path, ', ' )
                skinstool.addSkinSelection( skin, path )
        msg += "Done\n"

        msg += "OK\n"
    except:
        import sys
        msg += "Not done\n"
        msg += "Error: "+str(sys.exc_info()[0])+" "+str(sys.exc_info()[1])+" "+str(sys.exc_info()[2])+"\n"

    return msg

