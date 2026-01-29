Feature: Account registry

Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "Jimi", last name: "Hendrix", pesel: "89092909246"
    And I create an account using name: "Ryo", last name: "Fukui", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry
Scenario: User is able to update surname of already created account
    Given Acoount registry is empty
    And I create an account using name: "Female", last name: "Goat", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "La Femme"
    Then Account with pesel "95092909876" has "surname" equal to "La Femme"

Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "Yung", last name: "Lean", pesel: "95092909876"
    When I update "name" of account with pesel: "95092909876" to "Ghetto Dogs"
    Then Account with pesel "95092909876" has "name" equal to "Ghetto Dogs"

Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "Tampe", last name: "Chaser", pesel: "63080509876"
    Then Account with pesel "63080509876" exists in registry
    And Account with pesel "63080509876" has "name" equal to "Tampe"
    And Account with pesel "63080509876" has "surname" equal to "Chaser"
    And Number of accounts in registry equals: "1"

Scenario: User is able to delete created account
    Given Acoount registry is empty
    And I create an account using name: "cecil", last name: "fe", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

Scenario: User can make incoming transfer
    Given Account registry is empty
    And I create an account using name: "dsaf", last name: "fdsafasfdj", pesel: "40100909876"
    When I make "incoming" transfer of "100" to account with pesel: "40100909876"
    Then Transfer is accepted
    And Account with pesel "40100909876" has balance of "100"

Scenario: User can make outgoing transfer with sufficient balance
    Given Account registry is empty
    And I create an account using name: "cfecfe", last name: "fe", pesel: "42061809876"
    And I make "incoming" transfer of "200" to account with pesel: "42061809876"
    When I make "outgoing" transfer of "50" to account with pesel: "42061809876"
    Then Transfer is accepted
    And Account with pesel "42061809876" has balance of "150"

Scenario: User cannot make outgoing transfer with insufficient balance
    Given Account registry is empty
    And I create an account using name: "george", last name: "orwell", pesel: "43022509876"
    When I make "outgoing" transfer of "100" to account with pesel: "43022509876"
    Then Transfer is rejected
    And Account with pesel "43022509876" has balance of "0"

Scenario: User can make express transfer with fee
    Given Account registry is empty
    And I create an account using name: "Playboi", last name: "Carti", pesel: "40070709876"
    And I make "incoming" transfer of "100" to account with pesel: "40070709876"
    When I make "express" transfer of "50" to account with pesel: "40070709876"
    Then Transfer is accepted
    And Account with pesel "40070709876" has balance of "49"

Scenario: User cannot create account with already existing pesel
    Given Account registry is empty
    And I create an account using name: "john", last name: "lennon", pesel: "40100900000"
    When I create an account with duplicate pesel: "40100900000"
    Then Duplicate account creation is rejected
    And Number of accounts in registry equals: "1"

Scenario: Updating surname does not change the name
    Given Account registry is empty
    And I create an account using name: "Red", last name: "Army", pesel: "43072609876"
    When I update "surname" of account with pesel: "43072609876" to "richards"
    Then Account with pesel "43072609876" has "surname" equal to "richards"
    And Account with pesel "43072609876" has "name" equal to "mick"