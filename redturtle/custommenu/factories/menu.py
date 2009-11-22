# -*- coding: utf-8 -*-

from Acquisition import aq_inner, aq_parent

from plone.app.contentmenu.menu import FactoriesMenu as PloneFactoriesMenu
from plone.app.contentmenu.interfaces import IFactoriesMenu
from Products.CMFCore.utils import getToolByName

from OFS.interfaces import IFolder

from redturtle.custommenu.factories import custommenuMessageFactory as _

from zope.interface import implements
from zope.component import getMultiAdapter

class FactoriesMenu(PloneFactoriesMenu):
    implements(IFactoriesMenu)

    # Stolen from ploneview
    def isFolderOrFolderDefaultPage(self, context, request):
        context_state = getMultiAdapter((aq_inner(context), request), name=u'plone_context_state')
        return context_state.is_structural_folder() or context_state.is_default_page()

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = PloneFactoriesMenu.getMenuItems(self, context, request)

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
                results.append({'title'       : _(u'custommenu_manage_title', default=u'Customize menu\u2026'),
                                'description' : _(u'custommenu_manage_description', default=u'Manage custom elements of this menu'),
                                'action'      : context_url+'/@@customize-factoriesmenu',
                                'selected'    : False,
                                'icon'        : None,
                                'extra'       : {'id': 'settings', 'separator': None, 'class': ''},
                                'submenu'     : None,
                                'extra'       : {'separator': 'actionSeparator', 'id': 'customize-factoriesmenu', 'class': 'customize-menu'},
                                })
        return results

