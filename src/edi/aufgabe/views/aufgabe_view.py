# -*- coding: utf-8 -*-

from wtforms import Form
from wtforms.fields import TextAreaField, MultipleFileField
from wtforms.validators import InputRequired
from collective.wtforms.views import WTFormView
from wtforms.fields import MultipleFileField
from plone import api as ploneapi
from plone.app.textfield.value import RichTextValue

class SolutionForm(Form):
    text = TextAreaField("Beschreibung der Lösung", [InputRequired()])
    files = MultipleFileField("Upload von Dateien")


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

    def get_solution(self):
        if not self.homefolder:
            return
        aufgabeuid = self.context.UID()
        meineaufgabe_id = f'meine_aufgabe_{aufgabeuid}' 
        if meineaufgabe_id in self.homefolder:
            solution = {}
            import pdb;pdb.set_trace()
            meineaufgabe = self.homefolder[meineaufgabe_id]
            if meineaufgabe.text:
                solution['text'] = meineaufgabe.text.output
            brains = meineaufgabe.getFolderContents()
            if brains:
                solution['files'] = []
                for i in brains:
                    fileentry = {}
                    if i.portal_type == 'File':
                        fileentry['title'] = i.Title
                        fileentry['url'] = i.getURL()
                        solution['files'].append(fileentry)
            return solution
        return

    def get_group_solutions(self):
        if not self.authenticated:
            return
        aufgabeuid = self.context.UID()
        meineaufgabe_id = f'meine_aufgabe_{aufgabeuid}'
        brains = ploneapi.content.find(portal_type='MeineAufgabe', id=meineaufgabe_id)
        group_solutions = []
        for brain in brains:
            group_entry = {}
            meineaufgabe = brain.getObject()
            roles = ploneapi.user.get_roles(user=self.current, obj=meineaufgabe)
            if not 'Owner' in roles:
                group_entry['title'] = meineaufgabe.getOwner().getProperty('fullname')
                group_entry['url'] = meineaufgabe.absolute_url()
                group_entry['text'] = ''
                if meineaufgabe.text:
                    group_entry['text'] = meineaufgabe.text.output
                group_entry['files'] = []
                for fileentry in meineaufgabe.getFolderContents():
                    file_entry = {}
                    if fileentry.portal_type == 'File':
                        file_entry['title'] = fileentry.Title
                        file_entry['url'] = fileentry.getURL()
                        group_entry['files'].append(file_entry)
                group_solutions.append(group_entry)
        return group_solutions        


    def submit(self, button):
        if button == 'Speichern' and self.validate():
            if not self.homefolder:
                print('test')
                #message = 
                #return
            aufgabeuid = self.context.UID()
            meineaufgabe_id = f'meine_aufgabe_{aufgabeuid}'
            richtext = RichTextValue(raw=self.form.text.data,
                         mimeType='text/plain',
                         outputMimeType='text/html',
                         encoding='utf-8')
            obj = ploneapi.content.create(
                     type='MeineAufgabe',
                     id = meineaufgabe_id,
                     title=self.context.title,
                     text = richtext,
                     container=self.homefolder)
            import pdb;pdb.set_trace()
