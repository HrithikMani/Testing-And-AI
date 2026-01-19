@playwright
Feature: Playwright Documentation Website
  As a developer
  I want to navigate the Playwright docs
  So that I can learn how to use Playwright

  Background: Open Playwright website
    Given I am on the Playwright website

  @smoke
  Scenario: Verify homepage loads correctly
    Then I should see the page title contains "Playwright"
    And I should see the "Get started" link

  @theme
  Scenario: Toggle dark/light theme
    When I click the theme toggle button
    Then the theme should change

  @navigation
  Scenario: Navigate to documentation
    When I click on "Docs" in the navigation
    Then I should be on the documentation page
    And I should see the main content area

  @failure
  Scenario: Intentional failure - element not found
    Then I should see the "NonExistent Button That Does Not Exist" link

  @failure
  Scenario: Intentional failure - wrong page title
    Then I should see the page title contains "This Title Does Not Exist"
