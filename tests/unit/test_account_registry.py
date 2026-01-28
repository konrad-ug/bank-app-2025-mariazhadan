import pytest
from src.account import Account
from src.account_registry import AccountsRegistry

@pytest.fixture
def registry():
    reg = AccountsRegistry()
    acc1 = Account("Jan", "Kowalski", "90010112345")
    acc2 = Account("Anna", "Nowak", "85050554321")
    reg.add_account(acc1)
    reg.add_account(acc2)
    return reg, acc1, acc2

def test_add_account(registry):
    reg, acc1, acc2 = registry
    acc3 = Account("Piotr", "Zalewski", "92020298765")
    assert reg.count() == 2
    reg.add_account(acc3)
    assert reg.count() == 3

def test_find_by_pesel_found(registry):
    reg, acc1, acc2 = registry
    assert reg.find_by_pesel("90010112345") is acc1
    assert reg.find_by_pesel("85050554321") is acc2

def test_find_by_pesel_not_found(registry):
    reg, _, _ = registry
    assert reg.find_by_pesel("00000000000") is None

def test_get_all_accounts(registry):
    reg, acc1, acc2 = registry
    accounts = reg.all_accounts()
    assert acc1 in accounts
    assert acc2 in accounts
    assert len(accounts) == 2

def test_count(registry):
    reg, _, _ = registry
    acc3 = Account("Piotr", "Zalewski", "92020298765")
    assert reg.count() == 2
    reg.add_account(acc3)
    assert reg.count() == 3

def test_all_accounts_returns_new_list(registry):
    reg, _, _ = registry
    a = reg.all_accounts()
    b = reg.all_accounts()
    assert a is not b
    assert a == b

def test_remove_by_pesel_ok(registry):
    reg, acc1, _ = registry
    assert reg.count() == 2

    ok = reg.remove_by_pesel(acc1.pesel)
    assert ok is True
    assert reg.count() == 1
    assert reg.find_by_pesel(acc1.pesel) is None

def test_remove_by_pesel_missing(registry):
    reg, _, _ = registry
    before = (reg.count(), reg.all_accounts())
    ok = reg.remove_by_pesel("99999999999")
    assert ok is False
    assert reg.count() == before[0]
    assert reg.all_accounts() == before[1]

def test_remove_by_pesel_twice(registry):
    reg, acc1, _ = registry
    assert reg.remove_by_pesel(acc1.pesel) is True
    assert reg.remove_by_pesel(acc1.pesel) is False
