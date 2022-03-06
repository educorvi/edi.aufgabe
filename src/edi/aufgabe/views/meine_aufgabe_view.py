# -*- coding: utf-8 -*-
import magic
from wtforms import Form
from wtforms.fields import TextAreaField, MultipleFileField, RadioField
from wtforms.validators import InputRequired
from collective.wtforms.views import WTFormView
from plone import api as ploneapi
from plone.namedfile.file import NamedBlobFile
from plone.app.textfield.value import RichTextValue

class SolutionForm(Form):
    text = TextAreaField("Beschreibung der Lösung", [InputRequired()], render_kw={'class':'form-control'})
    public = RadioField("Wie soll die Lösung gespeichert werden?", choices=[('private','privat'), ('public','öffentlich')], default='private')
    files = MultipleFileField("Upload von Dateien", render_kw={'class':'form-control'})


class AufgabeView(WTFormView):
    formClass = SolutionForm
    buttons = ('Speichern', 'Abbrechen')

    def __call__(self):
        self.current = None
        self.homefolder = None
        self.authenticated = False
        membership = ploneapi.portal.get_tool(name='portal_membership')
        if not ploneapi.user.is_anonymous():
            self.authenticated = True
            self.current = ploneapi.user.get_current()
            self.homefolder = membership.getHomeFolder(self.current.getId())
        self.solution = self.get_solution()
        self.groupsolutions = self.get_group_solutions()
        if self.submitted:
            button = self.hasButtonSubmitted()
            if button:
                result = self.submit(button)
                if result:
                    return result
        return self.index()

