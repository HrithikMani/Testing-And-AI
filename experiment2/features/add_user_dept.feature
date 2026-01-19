@webchart @access_control
Feature: Add User Department
  As an administrator
  I want to manage departments and users
  So that I can organize access control effectively

  Background: Login and navigate to Access Control
    Given I am logged into WebChart
    And I click the "Control Panel" link
    And I click the "Access" charttab
    And I click the "Access Control" charttab subtab

  @add_department @smoke
  Scenario: Add a department and one user
    # Cleanup: Delete department if it exists from previous test runs
    Given I delete the "Testing" department if it exists
    When I click the "Add Department" link
    And I type "Testing" in the department name input
    And I uncheck all viewable departments
    And I check the "Testing" viewable department checkbox
    And I add user "Acardi" to the department
    And I click the "Submit Dept" button
    And I click the "Show All" link if visible
    Then I should see "Testing" listview link

  @add_more_users
  Scenario: Add more users to the Testing department
    Given I click the "Show All" link if visible
    When I click the "Testing" department edit link
    And I uncheck all viewable departments
    And I check the "Testing" viewable department checkbox
    And I add user "Butler" to the department
    And I add user "Morrison" to the department
    And I add user "Selenium" to the department
    And I add user "Garza" to the department
    And I add user "Thomas, Dave" to the department
    And I add user "Better Corp." to the department
    And I click the "Submit Dept" button
    Then I should see a success message

  @verify_users
  Scenario: Verify all users added to the new department
    Given I click the "Show All" link if visible
    When I click the "Testing" listview link
    Then I should see "Acardi" text
    And I should see "Better Corp." text
    And I should see "Butler" text
    And I should see "Garza" text
    And I should see "Morrison" text
    And I should see "Selenium" text
    And I should see "Thomas" text
