@search
Feature: Playwright Search Functionality
  As a developer
  I want to search the Playwright docs
  So that I can find specific information quickly

  Background: Open Playwright website
    Given I am on the Playwright website

  @smoke
  Scenario: Open search dialog
    When I click the search button
    Then I should see the search input
