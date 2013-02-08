from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from DateTime import DateTime


class transition(CatalogPathAware, SimpleItem):
    """ Links two activities """

    def __init__(self, id, From, To, condition='', description=''):
        if id == "":
            self.id = '%s_%s' % (From, To)
        else:
            self.id = id

        self.From = From
        self.To = To
        self.condition = condition
        self.description = description

    manage_options = ({'label': 'Edit', 'action': 'index_html'},)

    security = ClassSecurityInfo()


    security.declareProtected('Manage OpenFlow', 'manage_editTransitionForm')
    manage_editTransitionForm = PageTemplateFile('zpt/transition/manage_editTransitionForm', globals())


    meta_type = 'Transition'


    security.declareProtected('Manage OpenFlow', 'editTransition')
    def edit(self, condition, From, To, description, REQUEST=None):
        """  """
        self.condition = condition
        self.From = From
        self.To = To
        self.description = description
        self.reindex_object()
        if REQUEST: REQUEST.RESPONSE.redirect('../index_html')


InitializeClass(transition)
