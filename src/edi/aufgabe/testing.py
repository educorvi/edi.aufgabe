# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import edi.aufgabe


class EdiAufgabeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=edi.aufgabe)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edi.aufgabe:default')


EDI_AUFGABE_FIXTURE = EdiAufgabeLayer()


EDI_AUFGABE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDI_AUFGABE_FIXTURE,),
    name='EdiAufgabeLayer:IntegrationTesting',
)


EDI_AUFGABE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDI_AUFGABE_FIXTURE,),
    name='EdiAufgabeLayer:FunctionalTesting',
)


EDI_AUFGABE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EDI_AUFGABE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EdiAufgabeLayer:AcceptanceTesting',
)
