## Thanks to Ulrick Eck for the support

import Globals
from Globals import Persistent
from Acquisition import aq_inner, aq_parent
from AccessControl import getSecurityManager, ClassSecurityInfo
from Products.PageTemplates.Expressions import getEngine, _SecureModuleImporter

SecureModuleImporter = _SecureModuleImporter()

class Expression (Persistent):
    method_name = ''
    _expr = None

    security = ClassSecurityInfo()

    def __init__(self, method_name):
        self.method_name = method_name
        e = getEngine()
        self._expr = e.compile(method_name)

    security.declarePrivate('validate')
    def validate(self, inst, parent, name, value, md):
        # Zope 2.3.x
        return getSecurityManager().validate(inst, parent, name, value)

    def __call__(self, context):
       e = getEngine()
       if self._expr is None:
             self._expr = e.compile(self.method_name)
       c = e.getContext(context)
       return c.evaluate(self._expr)

Globals.InitializeClass(Expression)


def exprNamespace(client=None, form=None, field=None, value=None, object=None):
    c = { 'form': form,
          'field': field,
          'value': value,
          'here': object,
          'nothing': None,
          'options': {},
          'root': None,
          'request': None,
          'modules': SecureModuleImporter
        }
    return getEngine().getContext(c)

