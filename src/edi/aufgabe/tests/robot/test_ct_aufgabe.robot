# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s edi.aufgabe -t test_aufgabe.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src edi.aufgabe.testing.EDI_AUFGABE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/edi/aufgabe/tests/robot/test_aufgabe.robot
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

Scenario: As a site administrator I can add a Aufgabe
  Given a logged-in site administrator
    and an add Aufgabe form
   When I type 'My Aufgabe' into the title field
    and I submit the form
   Then a Aufgabe with the title 'My Aufgabe' has been created

Scenario: As a site administrator I can view a Aufgabe
  Given a logged-in site administrator
    and a Aufgabe 'My Aufgabe'
   When I go to the Aufgabe view
   Then I can see the Aufgabe title 'My Aufgabe'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Aufgabe form
  Go To  ${PLONE_URL}/++add++Aufgabe

a Aufgabe 'My Aufgabe'
  Create content  type=Aufgabe  id=my-aufgabe  title=My Aufgabe

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Aufgabe view
  Go To  ${PLONE_URL}/my-aufgabe
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Aufgabe with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Aufgabe title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
