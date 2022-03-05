# -*- coding: utf-8 -*-
from edi.aufgabe.content.meine_aufgabe import IMeineAufgabe  # NOQA E501
from edi.aufgabe.testing import EDI_AUFGABE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class MeineAufgabeIntegrationTest(unittest.TestCase):

    layer = EDI_AUFGABE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_meine_aufgabe_schema(self):
        fti = queryUtility(IDexterityFTI, name='MeineAufgabe')
        schema = fti.lookupSchema()
        self.assertEqual(IMeineAufgabe, schema)

    def test_ct_meine_aufgabe_fti(self):
        fti = queryUtility(IDexterityFTI, name='MeineAufgabe')
        self.assertTrue(fti)

    def test_ct_meine_aufgabe_factory(self):
        fti = queryUtility(IDexterityFTI, name='MeineAufgabe')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IMeineAufgabe.providedBy(obj),
            u'IMeineAufgabe not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_meine_aufgabe_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='MeineAufgabe',
            id='meine_aufgabe',
        )

        self.assertTrue(
            IMeineAufgabe.providedBy(obj),
            u'IMeineAufgabe not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('meine_aufgabe', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('meine_aufgabe', parent.objectIds())

    def test_ct_meine_aufgabe_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='MeineAufgabe')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_meine_aufgabe_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='MeineAufgabe')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'meine_aufgabe_id',
            title='MeineAufgabe container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
