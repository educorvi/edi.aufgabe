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
    files = MultipleFileField("Upload von Dateien", render_kw={'class':'form-control'})
    public = RadioField("Veröffentlichungsstatus der Lösung", choices=[('private','privat'), ('public','öffentlich')], default='private')


class MeineAufgabeView(WTFormView):
    formClass = SolutionForm
    buttons = ('Speichern', 'Zurück zur Aufgabe')

    def __call__(self):
        self.state = ploneapi.content.get_state(obj=self.context)
        self.current = None
        self.homefolder = None
        self.authenticated = False
        membership = ploneapi.portal.get_tool(name='portal_membership')
        if not ploneapi.user.is_anonymous():
            self.authenticated = True
            self.current = ploneapi.user.get_current()
            self.homefolder = membership.getHomeFolder(self.current.getId())
        if self.submitted:
            button = self.hasButtonSubmitted()
            if button:
                result = self.submit(button)
                if result:
                    return result
        return self.index()

    def renderForm(self):
        default_state = 'private'
        if self.state == 'internally_published':
            default_state = 'public'
        self.form.public.default = default_state
        self.form.process()
        return self.formTemplate()

    def text_edit_url(self):
        return self.context.absolute_url() + '/@@field_edit_form?fields=IRichTextBehavior.text'

    def get_files(self):
        files = []
        for i in self.context.getFolderContents():
            if i.portal_type == 'File':
                files.append(i.getObject())
        return files

    def get_aufgabe_url(self):
        aufgabe_uid = self.context.id.split('_')[-1]
        aufgabe = ploneapi.content.get(UID=aufgabe_uid)
        return aufgabe.absolute_url()

    def submit(self, button):
        if button == 'Speichern' and self.validate():
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
                                  container = self.context)
            public = self.form.public.data
            if public == 'private':
                if self.state == 'internally_published':
                    ploneapi.content.transition(self.context, transition='hide')
            elif public == 'public':
                if self.state == 'private':
                    ploneapi.content.transition(self.context, transition='publish_internally')
            url = self.context.absolute_url()
            ploneapi.portal.show_message(message='Ihre Lösung wurde in Ihrem Ordner gespeichert.', request=self.request, type='info')
            return self.request.response.redirect(url)
        url = self.get_aufgabe_url()
        return self.request.response.redirect(url)
