from behave import when, then, step
import requests

BASE_URL = "http://127.0.0.1:5000"
ACCOUNTS_URL = f"{BASE_URL}/api/accounts"


def _list_accounts():
    response = requests.get(ACCOUNTS_URL)
    return response.json()


def _delete_account(pesel):
    return requests.delete(f"{ACCOUNTS_URL}/{pesel}")


def _get_account(pesel):
    return requests.get(f"{ACCOUNTS_URL}/{pesel}")


def _create_account(name, surname, pesel):
    payload = {"name": name, "surname": surname, "pesel": pesel}
    return requests.post(ACCOUNTS_URL, json=payload)


@step("the account registry is empty")
def clear_account_registry(context):
    for account in _list_accounts():
        _delete_account(account["pesel"])


@step('I register an account with name "{name}", surname "{surname}", PESEL "{pesel}"')
def register_account(context, name, surname, pesel):
    create_resp = _create_account(name, surname, pesel)
    assert create_resp.status_code == 201


@when('I attempt to register another account with the same PESEL "{pesel}"')
def register_duplicate_account(context, pesel):
    context.create_resp = _create_account("dummy", "dummy", pesel)


@then("duplicate account creation is rejected")
def duplicate_creation_rejected(context):
    assert context.create_resp.status_code == 409


@step("the registry contains {count:d} account")
@step("the registry contains {count:d} accounts")
def registry_contains_count(context, count):
    accounts = _list_accounts()
    assert len(accounts) == int(count)


@step('an account with PESEL "{pesel}" exists')
def account_with_pesel_exists(context, pesel):
    response = _get_account(pesel)
    assert response.status_code == 200


@step('an account with PESEL "{pesel}" does not exist')
def account_with_pesel_missing(context, pesel):
    response = _get_account(pesel)
    assert response.status_code == 404


@when('I delete the account with PESEL "{pesel}"')
def delete_account(context, pesel):
    response = _delete_account(pesel)
    assert response.status_code == 200


@when('I change the "{field}" of the account with PESEL "{pesel}" to "{value}"')
def change_account_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    response = requests.patch(f"{ACCOUNTS_URL}/{pesel}", json={field: value})
    assert response.status_code == 200


@then('the account with PESEL "{pesel}" has "{field}" set to "{value}"')
def account_field_equals(context, pesel, field, value):
    response = _get_account(pesel)
    assert response.status_code == 200
    account = response.json()
    assert account[field] == value


@when('I make an {transfer_type} transfer of {amount:g} to the account with PESEL "{pesel}"')
@step('I make an {transfer_type} transfer of {amount:g} to the account with PESEL "{pesel}"')
def make_transfer(context, transfer_type, amount, pesel):
    payload = {"type": transfer_type, "amount": float(amount)}
    response = requests.post(f"{ACCOUNTS_URL}/{pesel}/transfer", json=payload)
    context.transfer_response = response


@then("the transfer is accepted")
def transfer_accepted(context):
    assert context.transfer_response.status_code == 200


@then("the transfer is rejected")
def transfer_rejected(context):
    assert context.transfer_response.status_code == 422


@then('the account with PESEL "{pesel}" has balance {balance:g}')
def account_balance_equals(context, pesel, balance):
    response = _get_account(pesel)
    assert response.status_code == 200
    account = response.json()
    assert account["balance"] == float(balance)
