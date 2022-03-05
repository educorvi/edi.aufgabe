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
    text = RichText(title="Text der Lösung")


@implementer(IAufgabe)
class Aufgabe(Container):
    """
    """
