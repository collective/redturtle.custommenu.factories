# -*- coding: utf-8 -*-

from zope.interface import implements, alsoProvides
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from redturtle.custommenu.factories.interfaces import ICustomMenuEnabled

ANN_CUSTOMMENU_KEY = 'redturtle.custommenu.factories.elements'

class CustomizeFactoriesMenu(BrowserView):
    """View for managing custom factories menu"""

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        request.set('disable_border', True)

    template = ViewPageTemplateFile('view.pt')

    def addMenuEntry(self, form):
        context = self.context
        alsoProvides(context, ICustomMenuEnabled)
        context.reindexObject('object_provides')
        # now storing the data
        annotations = IAnnotations(context)
        
        # BBB: to be continued
        
        return "{'response':'added'}"
    
    def __call__(self):
        request = self.request
        context = self.context
        if request.form.get("action",'')=='add':
            request.response.setHeader('Content-Type','application/json')
            return self.addMenuEntry(request.form)
        return self.template()
