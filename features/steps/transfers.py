from behave import given, when, then
import requests

BASE_URL = "http://127.0.0.1:5000"
ACCOUNTS_URL = f"{BASE_URL}/api/accounts"
TIMEOUT = 5


def _json_ok(response):
    return response.ok and response.headers.get("Content-Type", "").startswith("application/json")


def _clear_registry():
    response = requests.get(ACCOUNTS_URL, timeout=TIMEOUT)
    if _json_ok(response):
        for account in response.json():
            requests.delete(f"{ACCOUNTS_URL}/{account['pesel']}", timeout=TIMEOUT)


def _ensure_account(pesel, name="BDD", surname="User"):
    payload = {"name": name, "surname": surname, "pesel": pesel}
    response = requests.post(ACCOUNTS_URL, json=payload, timeout=TIMEOUT)
    assert response.status_code in (201, 409), f"Create failed: {response.status_code}"


def _balance_for(pesel) -> float:
    response = requests.get(f"{ACCOUNTS_URL}/{pesel}", timeout=TIMEOUT)
    assert response.status_code == 200
    return float(response.json()["balance"])


def _seed_balance(pesel, target):
    _clear_registry()
    _ensure_account(pesel)
    if float(target) > 0:
        response = requests.post(
            f"{ACCOUNTS_URL}/{pesel}/transfer",
            json={"type": "incoming", "amount": float(target)},
            timeout=TIMEOUT,
        )
        assert response.status_code == 200, f"Failed to seed balance: {response.status_code}"


@given("a user has a bank account with PESEL {pesel}")
def user_has_account(context, pesel):
    _ensure_account(pesel)
    context.pesel = pesel


@given("the account balance is {amount:g} PLN")
def account_balance_is(context, amount):
    assert hasattr(context, "pesel"), "PESEL is missing from context"
    _seed_balance(context.pesel, amount)


@when("the user receives an incoming transfer of {amount:g} PLN")
def incoming_transfer(context, amount):
    response = requests.post(
        f"{ACCOUNTS_URL}/{context.pesel}/transfer",
        json={"type": "incoming", "amount": float(amount)},
        timeout=TIMEOUT,
    )
    context.last_response = response


@when("the user submits an outgoing transfer of {amount:g} PLN")
def outgoing_transfer(context, amount):
    response = requests.post(
        f"{ACCOUNTS_URL}/{context.pesel}/transfer",
        json={"type": "outgoing", "amount": float(amount)},
        timeout=TIMEOUT,
    )
    context.last_response = response


@when("the user submits an express transfer of {amount:g} PLN")
def express_transfer(context, amount):
    response = requests.post(
        f"{ACCOUNTS_URL}/{context.pesel}/transfer",
        json={"type": "express", "amount": float(amount)},
        timeout=TIMEOUT,
    )
    context.last_response = response


@when("the user submits a transfer with invalid type {kind}")
def invalid_transfer_type(context, kind):
    response = requests.post(
        f"{ACCOUNTS_URL}/{context.pesel}/transfer",
        json={"type": kind, "amount": 1},
        timeout=TIMEOUT,
    )
    context.last_response = response
    context.kind = kind


@then("the system should respond with: Transfer accepted")
def response_transfer_accepted(context):
    assert context.last_response.status_code == 200


@then("the system should respond with: Insufficient funds")
def response_insufficient_funds(context):
    assert context.last_response.status_code == 422


@then("the system should respond with: Unknown transfer type {kind}")
def response_unknown_type(context, kind):
    assert context.last_response.status_code == 400
    try:
        message = context.last_response.json().get("message", "").lower()
        assert "type" in message or "unknown" in message or "doesn`t" in message
    except Exception:
        pass


@then("the account balance should be {expected:g} PLN")
def account_balance_should_be(context, expected):
    balance = _balance_for(context.pesel)
    assert abs(balance - float(expected)) < 1e-6, f"Expected {expected}, got {balance}"
