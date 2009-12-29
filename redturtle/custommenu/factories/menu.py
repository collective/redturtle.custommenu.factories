# -*- coding: utf-8 -*-

from Acquisition import aq_inner, aq_parent
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.contentmenu.menu import FactoriesMenu as PloneFactoriesMenu
from plone.app.contentmenu.interfaces import IFactoriesMenu
from Products.CMFCore.utils import getToolByName

from OFS.interfaces import IFolder

from redturtle.custommenu.factories import custommenuMessageFactory as _
from redturtle.custommenu.factories.browser.view import ANN_CUSTOMMENU_KEY

from Products.PageTemplates import Expressions
from Products.PageTemplates.TALES import CompilerError

class FactoriesMenu(PloneFactoriesMenu):
    implements(IFactoriesMenu)

    # Stolen from ploneview
    def isFolderOrFolderDefaultPage(self, context, request):
        context_state = getMultiAdapter((aq_inner(context), request), name=u'plone_context_state')
        return context_state.is_structural_folder() or context_state.is_default_page()

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = PloneFactoriesMenu.getMenuItems(self, context, request)
        portal = getToolByName(context, 'portal_url').getPortalObject()

        # now put there local customizations (if any)
        talEngine = Expressions.getEngine()
        data = {'context': context, 'portal': portal}

        saved_customizations = self._getSavedCustomizations(context)
        for c in saved_customizations:
            condition = c['condition-tales']
            if condition:
                compiledCondition = talEngine.compile(condition)
                try:
                    result = compiledCondition(talEngine.getContext(data))
                except KeyError, inst:
                    print inst
                    continue
                if result:
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
                        results.append(self._formatNewEntry(c, compiledURL, compiledIcon))

        if IFolder.providedBy(context):
            folder = context
        elif self.isFolderOrFolderDefaultPage(context, request):
            folder = aq_parent(aq_inner(context))
        else:
            folder = None

        if folder:
            mtool = getToolByName(context, 'portal_membership')
            if not mtool.isAnonymousUser() and mtool.getAuthenticatedMember().has_permission('Customize menu: factories', folder):
                context_url = folder.absolute_url()
                results.append({'title'       : _(u'custommenu_manage_title', default=_(u'Customize menu\u2026')),
                                'description' : _(u'custommenu_manage_description', default=_(u'Manage custom elements of this menu')),
                                'action'      : context_url+'/@@customize-factoriesmenu',
                                'selected'    : False,
                                'icon'        : None,
                                'submenu'     : None,
                                'extra'       : {'separator': 'actionSeparator', 'id': 'customize-factoriesmenu', 'class': 'customize-menu'},
                                })
        return results

    def _formatNewEntry(self, customization, url, icon):
        """Return a menu-like structure with the new additional element"""
        return {'title'       : _(customization['element-name']),
                'description' : _(customization['element-descr']),
                'action'      : url,
                'selected'    : False,
                'icon'        : icon,
                'submenu'     : None,
                'extra'       : {'separator': None, 'id': '', 'class': ''},
                }

    def _getSavedCustomizations(self, context):
        annotations = IAnnotations(context)
        if annotations.has_key(ANN_CUSTOMMENU_KEY):
            return annotations[ANN_CUSTOMMENU_KEY]
        return []
