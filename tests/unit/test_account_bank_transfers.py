import pytest
from src.account import Account

@pytest.fixture
def account():
    return Account("Vietnam", "War", "12345678901")

class TestAccount_BankTransfers:
    def test_history_receive_transfer(self, account):
        account.receive_transfer(500)
        assert account.history == [500.0]

    def test_history_send_transfer(self, account):
        account.balance = 1000
        account.send_transfer(300)
        assert account.history == [-300.0]

    def test_history_send_express_transfer(self, account):
        account.balance = 1000
        account.send_express_transfer(300)
        assert account.history == [-300.0, -1.0]

    def test_history_multiple_operations(self, account):
        account.receive_transfer(500)
        account.send_express_transfer(300)
        assert account.history == [500.0, -300.0, -1.0]

    def test_submit_for_loan_last_three_positive(self, account):
        account.receive_transfer(100)
        account.receive_transfer(200)
        account.receive_transfer(300)
        prev_balance = account.balance
        assert account.submit_for_loan(150) is True
        assert account.balance == prev_balance + 150

    def test_submit_for_loan_last_five_sum_gt_amount(self, account):
        account.receive_transfer(100)
        account.send_transfer(50)
        account.receive_transfer(200)
        account.send_express_transfer(30)  # -30, -1
        account.receive_transfer(500)
        prev_balance = account.balance
        assert account.submit_for_loan(100) is True
        assert account.balance == prev_balance + 100

    def test_submit_for_loan_conditions_not_met(self, account):
        account.receive_transfer(100)
        account.send_transfer(50)
        account.send_transfer(20)
        prev_balance = account.balance
        assert account.submit_for_loan(500) is False
        assert account.balance == prev_balance

    @pytest.mark.parametrize("bad_amount", [0, -10, "abc", None])
    def test_submit_for_loan_invalid_amount(self, account, bad_amount):
        assert account.submit_for_loan(bad_amount) is False

    def test_last_three_positive(self, account):
        assert account._last_three_positive() is False
        account.receive_transfer(10)
        account.receive_transfer(20)
        assert account._last_three_positive() is False
        account.receive_transfer(30)
        assert account._last_three_positive() is True
        account.send_transfer(5)
        assert account._last_three_positive() is False

@pytest.mark.parametrize(
    "value, expected",
    [
        (10, 10.0),
        (3.14, 3.14),
        ("2.5", 2.5),
        ("0", 0.0),
        ("-1", -1.0),
    ],
)
def test_coerce_amount_valid(value, expected):
    acc = Account("A", "B", "12345678901")
    assert acc._coerce_amount(value) == expected

@pytest.mark.parametrize("value", ["abc", "12a", None, [], {}, object()])
def test_coerce_amount_invalid(value):
    acc = Account("A", "B", "12345678901")
    assert acc._coerce_amount(value) is None
