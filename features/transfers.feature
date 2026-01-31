Feature: Transfer processing

@transfer
Scenario: Incoming transfer succeeds
    Given a user has a bank account with PESEL 98765432109
    And the account balance is 1000 PLN
    When the user receives an incoming transfer of 500 PLN
    Then the account balance should be 1500 PLN

@transfer
Scenario: Outgoing transfer succeeds
    Given a user has a bank account with PESEL 98765432109
    And the account balance is 1000 PLN
    When the user submits an outgoing transfer of 300 PLN
    Then the system should respond with: Transfer accepted
    And the account balance should be 700 PLN

@transfer
Scenario: Express transfer succeeds
    Given a user has a bank account with PESEL 98765432109
    And the account balance is 2000 PLN
    When the user submits an express transfer of 1000 PLN
    Then the system should respond with: Transfer accepted
    And the account balance should be 999 PLN

@transfer
Scenario: Outgoing transfer fails due to insufficient funds
    Given a user has a bank account with PESEL 98765432109
    And the account balance is 200 PLN
    When the user submits an outgoing transfer of 500 PLN
    Then the system should respond with: Insufficient funds
    And the account balance should be 200 PLN

@transfer
Scenario: Express transfer fails due to insufficient funds
    Given a user has a bank account with PESEL 98765432109
    And the account balance is 300 PLN
    When the user submits an express transfer of 1000 PLN
    Then the system should respond with: Insufficient funds
    And the account balance should be 300 PLN

@transfer
Scenario: Invalid transfer type
    Given a user has a bank account with PESEL 98765432109
    And the account balance is 1000 PLN
    When the user submits a transfer with invalid type superfast
    Then the system should respond with: Unknown transfer type superfast
    And the account balance should be 1000 PLN
