@api
Feature: Playwright API Documentation
  As a developer
  I want to browse the API documentation
  So that I can learn the Playwright API

  Background: Open Playwright website
    Given I am on the Playwright website

  Scenario: Navigate to API reference
    When I click on "API" in the navigation
    Then I should see the heading "Playwright Library"
