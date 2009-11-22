# -*- coding: utf-8 -*-

from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class CustomizeFactoriesMenu(BrowserView):
    """Form for managin custom factories menu"""

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        request.set('disable_border', True)

    __call__ = ViewPageTemplateFile('view.pt')