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

    def get_solution(self):
        if not self.homefolder:
            return
        aufgabeuid = self.context.UID()
        meineaufgabe_id = f'meine_aufgabe_{aufgabeuid}' 
        if meineaufgabe_id in self.homefolder:
            solution = {}
            meineaufgabe = self.homefolder[meineaufgabe_id]
            if meineaufgabe.text:
                solution['text'] = meineaufgabe.text.output
            brains = meineaufgabe.getFolderContents()
            solution['files'] = []
            for i in brains:
                fileentry = {}
                if i.portal_type == 'File':
                    fileobj = i.getObject()
                    fileentry['title'] = fileobj.title
                    fileentry['url'] = '%s/@@download/file/%s' %(fileobj.absolute_url(), fileobj.file.filename)
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
            for file in self.form.files.data:
                mime = magic.Magic(mime=True)
                content_type = mime.from_buffer(file.file.read())
                if content_type != 'application/x-empty':
                    file.file.seek(0)
                    uploadname = file.filename
                    upload = NamedBlobFile(data=file.file.read(), contentType=content_type, filename=uploadname)
                    newfile = ploneapi.content.create(
                                  type="File",
                                  title=uploadname,
                                  file = upload,
                                  container = obj)
            if self.form.public.data == 'public':
                ploneapi.content.transition(obj, transition='publish_internally')
            url = self.context.absolute_url()
            ploneapi.portal.show_message(message='Ihre Lösung wurde in Ihrem Ordner gespeichert.', request=self.request, type='info')
            return self.request.response.redirect(url)
        ploneapi.portal.show_message(message='Bearbeiten der Lösung abgebrochen.', request=self.request, type='info')
        url = self.context.absolute_url()
        return self.request.response.redirect(url)
