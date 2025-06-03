Feature: pessoa/ crud

  Scenario: Register a person successfully
    Given I have a client and a CPF "12345678901"
    When I try to register this CPF
    Then I should receive a success message

  Scenario: Try to register the same CPF again
    Given I have a client and a CPF "12312312300"
    When I try to register this CPF
    Then I should receive an error message

  Scenario: List all registered people
    Given I have a registered person with CPF "11122233344"
    When I visit the list page
    Then I should see the person with CPF "11122233344"

  Scenario: Edit a registered person
    Given I have a registered person with CPF "22233344455"
    When I edit the person's name to "Updated"
    Then I should see the person with name "Updated"

  Scenario: Remove a registered person
    Given I have a registered person with CPF "33344455566"
    When I remove the person
    Then I should not see the person with CPF "33344455566"
