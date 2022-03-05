# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.aufgabe -t test_meine_aufgabe.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.aufgabe.testing.EDI_AUFGABE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/aufgabe/tests/robot/test_meine_aufgabe.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a MeineAufgabe
  Given a logged-in site administrator
    and an add MeineAufgabe form
   When I type 'My MeineAufgabe' into the title field
    and I submit the form
   Then a MeineAufgabe with the title 'My MeineAufgabe' has been created

Scenario: As a site administrator I can view a MeineAufgabe
  Given a logged-in site administrator
    and a MeineAufgabe 'My MeineAufgabe'
   When I go to the MeineAufgabe view
   Then I can see the MeineAufgabe title 'My MeineAufgabe'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add MeineAufgabe form
  Go To  ${PLONE_URL}/++add++MeineAufgabe

a MeineAufgabe 'My MeineAufgabe'
  Create content  type=MeineAufgabe  id=my-meine_aufgabe  title=My MeineAufgabe

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the MeineAufgabe view
  Go To  ${PLONE_URL}/my-meine_aufgabe
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a MeineAufgabe with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the MeineAufgabe title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
