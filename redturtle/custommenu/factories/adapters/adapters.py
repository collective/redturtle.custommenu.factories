# -*- coding: utf-8 -*-

from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from redturtle.custommenu.factories.interfaces import ICustomFactoryMenuProvider

class FolderFactoryMenuAdapter(object):
    implements(ICustomFactoryMenuProvider)

    def __init__(self, context):
        self.context = context

    def foo(self):
        print "A folder!"

class PloneSiteFactoryMenuAdapter(object):
    implements(ICustomFactoryMenuProvider)

    def __init__(self, context):
        self.context = context

    def foo(self):
        print "The Plone site!"