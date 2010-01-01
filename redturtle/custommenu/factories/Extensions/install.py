# -*- coding: utf-8 -*-

from zope import interface
from redturtle.custommenu.factories.interfaces import ICustomMenuEnabled
from redturtle.custommenu.factories.browser.view import ANN_CUSTOMMENU_KEY

def install(portal):
    setup_tool = portal.portal_setup
    setup_tool.setImportContext('profile-redturtle.custommenu.factories:default')
    setup_tool.runAllImportSteps()

def uninstall(portal, reinstall=False):
    setup_tool = portal.portal_setup
    setup_tool.setImportContext('profile-redturtle.custommenu.factories:uninstall')
    setup_tool.runAllImportSteps()
    
    if not reinstall:
        cleanMenuCustomizations(portal)

def cleanMenuCustomizations(portal):
    """Remove all customization from the Plone site"""
    catalog = portal.portal_catalog
    results = catalog(object_provides=ICustomMenuEnabled.__identifier__)
    for x in results:
        obj = x.getObject()
        interface.noLongerProvides(obj, ICustomMenuEnabled)
        print 'Removing customization of the "Add new..." menu at %s' % x.getPath()
        obj.reindexObject(['object_provides'])
    # Also the Plone site can be customized... check manually as it isn't in the catalog
    if ICustomMenuEnabled.providedBy(portal):
        interface.noLongerProvides(portal, ICustomMenuEnabled)
        print 'Removing customization of the "Add new..." menu at the Plone site'
        