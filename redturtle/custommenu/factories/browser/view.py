# -*- coding: utf-8 -*-

from zope.interface import implements, alsoProvides
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from redturtle.custommenu.factories import custommenuMessageFactory as _

from redturtle.custommenu.factories.interfaces import ICustomMenuEnabled

ANN_CUSTOMMENU_KEY = 'redturtle.custommenu.factories.elements'

class CustomizeFactoriesMenu(BrowserView):
    """View for managing custom factories menu"""

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        request.set('disable_border', True)

    template = ViewPageTemplateFile('view.pt')

    def _addMenuEntry(self, form):
        context = self.context
        alsoProvides(context, ICustomMenuEnabled)
        context.reindexObject('object_provides')
        
        saved_customizations = self._getSavedCustomizations()
        saved_customizations.append({'index': len(saved_customizations),
                                     'element-name': form.get('element-name'),
                                     'element-descr': form.get('element-descr'),
                                     'icon-tales': form.get('icon-tales'),
                                     'condition-tales': form.get('condition-tales'),
                                     'element-tales': form.get('element-tales'),
                                     })
        
        annotations = IAnnotations(context)
        annotations[ANN_CUSTOMMENU_KEY] = saved_customizations
        annotations._p_changed=1
        return _(u'New entry added')

    def _deleteMenuEntries(self, form):
        context = self.context
        saved_customizations = self._getSavedCustomizations()

        to_delete = form.get('delete',[])
        saved_customizations = [x for x in saved_customizations if x['index'] not in to_delete]
        self._reindex(saved_customizations)
        
        annotations = IAnnotations(context)
        annotations[ANN_CUSTOMMENU_KEY] = saved_customizations
        annotations._p_changed=1
        return _(u'Customization/s removed')


    def _getSavedCustomizations(self):
        context = self.context
        annotations = IAnnotations(context)
        if annotations.has_key(ANN_CUSTOMMENU_KEY):
            return annotations[ANN_CUSTOMMENU_KEY]
        return []

    def listCustomizations(self):
        """Return all saved customization to be shown in the template"""
        return self._getSavedCustomizations()
        
    def _reindex(self, customizations_list):
        """Fix all index inside a customizations structure.
        @return: the customization list itself
        """
        for x in range(0, len(customizations_list)):
            customizations_list[x]['index'] = x
        return customizations_list
    
    def __call__(self):
        request = self.request
        context = self.context
        plone_utils = getToolByName(context, 'plone_utils')
        message = None
        if request.form.get("add-command",''):
            # request.response.setHeader('Content-Type','application/json')
            message = self._addMenuEntry(request.form)
            request.response.redirect(context.absolute_url()+'/@@customize-factoriesmenu')
            return
        if request.form.get("delete-command",''):
            # request.response.setHeader('Content-Type','application/json')
            message = self._deleteMenuEntries(request.form)
            request.response.redirect(context.absolute_url()+'/@@customize-factoriesmenu')
            return        
        if message:
            plone_utils.addPortalMessage(message, type='info')
        return self.template()
