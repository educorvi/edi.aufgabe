# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import implementer

from edi.aufgabe import _

class IAufgabe(model.Schema):
    """ Marker interface and Dexterity Python Schema for Aufgabe
    """
    share = schema.Bool(title="Lernende dürfen die Lösungen anderer Kursteilnehmer erst sehen, wenn die eigene Lösung ebenfalls veröffentlicht  wurde.") 

@implementer(IAufgabe)
class Aufgabe(Container):
    """
    """
