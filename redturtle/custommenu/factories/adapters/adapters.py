# -*- coding: utf-8 -*-

from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from redturtle.custommenu.factories.interfaces import ICustomFactoryMenuProvider
from redturtle.custommenu.factories import custommenuMessageFactory as _

from Products.PageTemplates import Expressions
from Products.PageTemplates.TALES import CompilerError

from zope.component import getMultiAdapter

class MenuCoreAdapter(object):

    def __init__(self, context):
        self.context = context

    def _formatNewEntry(self, customization, url, icon):
        """Return a menu-like structure with the new additional element"""
        return {'title'       : _(customization['element-name']),
                'description' : _(customization['element-descr']),
                'action'      : url,
                'selected'    : False,
                'icon'        : icon,
                'submenu'     : None,
                'extra'       : {'separator': None, 'id': customization['element-id'], 'class': ''},
                }

    def getMenuCustomization(self, context, folder, results):
        raise NotImplementedError("You must provide the getMenuCustomization method")

class FolderFactoryMenuAdapter(MenuCoreAdapter):
    implements(ICustomFactoryMenuProvider)

class PloneSiteFactoryMenuAdapter(MenuCoreAdapter):
    implements(ICustomFactoryMenuProvider)

    def getMenuCustomization(self, context, folder, results):
        """Get saved menu customization from this context"""
        portal_url = getToolByName(context, 'portal_url')
        talEngine = Expressions.getEngine()
        data = {'context': context, 'portal_url': portal_url, 'container': folder}

        view = getMultiAdapter((folder, folder.REQUEST), name=u'customize-factoriesmenu')

        newResults = []
        newIds = []
        extras, saved_customizations = view.getSavedCustomizations()
        for c in saved_customizations:
            condition = c['condition-tales']
            if condition:
                compiledCondition = talEngine.compile(condition)
                try:
                    result = compiledCondition(talEngine.getContext(data))
                except KeyError, inst:
                    print inst
                    continue
                if not result:
                    continue

            # URL
            url = talEngine.compile(c['element-tales'])
            try:
                compiledURL = url(talEngine.getContext(data))
            except KeyError, inst:
                print inst
                continue
            # ICON
            icon = talEngine.compile(c['icon-tales'])
            try:
                compiledIcon = icon(talEngine.getContext(data))
            except KeyError, inst:
                print inst
                compiledIcon = None
            
            if compiledURL:
                newElement = self._formatNewEntry(c, compiledURL, compiledIcon)
                if newElement['extra']['id']:
                    newIds.append(newElement['extra']['id'])
                newResults.append(newElement)

        # Spit off overriden elements, using id
        results = [x for x in results if x['extra']['id'] not in newIds]
        results.extend(newResults)
        return results
