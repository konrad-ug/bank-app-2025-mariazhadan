Feature: Account registry

Scenario: User can create two accounts
    Given the account registry is empty
    When I register an account with name "Jimi", surname "Hendrix", PESEL "89092909246"
    And I register an account with name "Ryo", surname "Fukui", PESEL "79101011234"
    Then the registry contains 2 accounts
    And an account with PESEL "89092909246" exists
    And an account with PESEL "79101011234" exists

Scenario: User can update the surname of an existing account
    Given the account registry is empty
    And I register an account with name "Female", surname "Goat", PESEL "95092909876"
    When I change the "surname" of the account with PESEL "95092909876" to "La Femme"
    Then the account with PESEL "95092909876" has "surname" set to "La Femme"

Scenario: User can update the name of an existing account
    Given the account registry is empty
    And I register an account with name "Yung", surname "Lean", PESEL "95092909876"
    When I change the "name" of the account with PESEL "95092909876" to "Ghetto Dogs"
    Then the account with PESEL "95092909876" has "name" set to "Ghetto Dogs"

Scenario: New account has all fields set
    Given the account registry is empty
    When I register an account with name "Tampe", surname "Chaser", PESEL "63080509876"
    Then an account with PESEL "63080509876" exists
    And the account with PESEL "63080509876" has "name" set to "Tampe"
    And the account with PESEL "63080509876" has "surname" set to "Chaser"
    And the registry contains 1 account

Scenario: User can delete an account
    Given the account registry is empty
    And I register an account with name "cecil", surname "fe", PESEL "01092909876"
    When I delete the account with PESEL "01092909876"
    Then an account with PESEL "01092909876" does not exist
    And the registry contains 0 accounts

Scenario: User can make an incoming transfer
    Given the account registry is empty
    And I register an account with name "dsaf", surname "fdsafasfdj", PESEL "40100909876"
    When I make an incoming transfer of 100 to the account with PESEL "40100909876"
    Then the transfer is accepted
    And the account with PESEL "40100909876" has balance 100

Scenario: User can make an outgoing transfer with sufficient balance
    Given the account registry is empty
    And I register an account with name "cfecfe", surname "fe", PESEL "42061809876"
    And I make an incoming transfer of 200 to the account with PESEL "42061809876"
    When I make an outgoing transfer of 50 to the account with PESEL "42061809876"
    Then the transfer is accepted
    And the account with PESEL "42061809876" has balance 150

Scenario: User cannot make an outgoing transfer with insufficient balance
    Given the account registry is empty
    And I register an account with name "george", surname "orwell", PESEL "43022509876"
    When I make an outgoing transfer of 100 to the account with PESEL "43022509876"
    Then the transfer is rejected
    And the account with PESEL "43022509876" has balance 0

Scenario: User can make an express transfer with a fee
    Given the account registry is empty
    And I register an account with name "Playboi", surname "Carti", PESEL "40070709876"
    And I make an incoming transfer of 100 to the account with PESEL "40070709876"
    When I make an express transfer of 50 to the account with PESEL "40070709876"
    Then the transfer is accepted
    And the account with PESEL "40070709876" has balance 49

Scenario: User cannot create an account with an existing PESEL
    Given the account registry is empty
    And I register an account with name "john", surname "lennon", PESEL "40100900000"
    When I attempt to register another account with the same PESEL "40100900000"
    Then duplicate account creation is rejected
    And the registry contains 1 account

Scenario: Updating the surname does not change the name
    Given the account registry is empty
    And I register an account with name "Red", surname "Army", PESEL "43072609876"
    When I change the "surname" of the account with PESEL "43072609876" to "richards"
    Then the account with PESEL "43072609876" has "surname" set to "richards"
    And the account with PESEL "43072609876" has "name" set to "Red"
