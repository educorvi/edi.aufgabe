# edi.aufgabe

Mit diesem Plone-Add-On können Aufgaben zu einem Standard-Plone-Ordner zu einem Crashkurs 
(edi.crashkurs) oder zur einem Plone-Course (edi.plonecourse) hinzugefügt werden. Für die Lösung
einer Aufgabe wird ein Artikel "MeineAufgabe" im persönlichen Ordner des Benutzers angelegt.

## Leistungsmerkmale

- Beschreibung einer Aufgabe in Plone
- für die Lösung der Aufgabe wird ein Artikel "MeineAufgabe" im persönlichen Ordner des Benutzers abgelegt
- die Lösung wird im Kontext der Aufgabe anzeigt
- die Bearbeitung der Aufgabe erfolgt im Kontext von "MeinOrdner"
- die Benutzer können entscheiden, ob die eigene Lösung veröffentlicht (geteilt) werden soll
- die öffentlichen Lösungen anderer Kursteilnehmer werden in einem Akkordeon unter der eigenen Lösung dargestellt.

Examples
--------

This add-on can be seen in action at the following sites:
- Is there a page on the internet where everybody can see the features?


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://docs.plone.org/foo/bar


Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Installation
------------

Install edi.aufgabe by adding it to your buildout::

    [buildout]

    ...

    eggs =
        edi.aufgabe


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/edi.aufgabe/issues
- Source Code: https://github.com/collective/edi.aufgabe
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
