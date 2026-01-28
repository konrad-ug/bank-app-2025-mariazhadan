from src.business_account import CompanyAccount
import pytest


class TestCompanyAccount:

    def test_create_company_account_valid_nip(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        assert account.company_name == "Tech Corp"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_create_company_account_invalid_nip_short(self):
        account = CompanyAccount("ABC Company", "123456789")
        assert account.nip == "Invalid"

    def test_create_company_account_invalid_nip_long(self):
        account = CompanyAccount("XYZ Ltd", "12345678901")
        assert account.nip == "Invalid"

    def test_create_company_account_invalid_nip_letters(self):
        account = CompanyAccount("Test Corp", "123ABC7890")
        assert account.nip == "Invalid"

    def test_company_account_receive_transfer(self):
        account = CompanyAccount("Transfer Co", "1234567890")
        result = account.receive_transfer(1000.0)
        assert result == True
        assert account.balance == 1000.0

    def test_company_account_send_transfer(self):
        account = CompanyAccount("Sender Co", "1234567890")
        account.receive_transfer(1000.0)
        result = account.send_transfer(300.0)
        assert result == True
        assert account.balance == 700.0

    def test_company_account_send_transfer_insufficient_funds(self):
        account = CompanyAccount("Poor Co", "1234567890")
        account.receive_transfer(100.0)
        result = account.send_transfer(500.0)
        assert result == False
        assert account.balance == 100.0

    def test_create_invalid_nip_letters(self):
        acc = CompanyAccount("Test Corp", "123ABC7890")
        assert acc.nip == "Invalid"

    def test_receive_transfer_positive_amount(self):
        acc = CompanyAccount("Receiver Co", "1234567890")
        assert acc.receive_transfer(500.0) is True
        assert acc.balance == 500.0

    def test_receive_transfer_negative_amount(self):
        acc = CompanyAccount("Receiver Co", "1234567890")
        assert acc.receive_transfer(-50) is False
        assert acc.balance == 0.0

    def test_receive_transfer_invalid_type(self):
        acc = CompanyAccount("Receiver Co", "1234567890")
        assert acc.receive_transfer("abc") is False
        assert acc.balance == 0.0
    
    def test_send_transfer_negative_amount(self):
        acc = CompanyAccount("Sender Co", "1234567890")
        acc.receive_transfer(100.0)
        assert acc.send_transfer(-50) is False
        assert acc.balance == 100.0
    
    def test_send_transfer_invalid_type(self):
        acc = CompanyAccount("Sender Co", "1234567890")
        acc.receive_transfer(100.0)
        assert acc.send_transfer("abc") is False
        assert acc.balance == 100.0
    
    def test_company_get_express_fee(self):
        acc = CompanyAccount("Fee Co", "1234567890")
        fee = acc.get_express_fee()
        assert fee == 5.0


@pytest.fixture
def firm_account():
    acc = CompanyAccount()
    acc.balance = 5000
    acc.history = [1000, -1775, 2000]  
    return acc

def test_take_loan_success(firm_account):
    prev_balance = firm_account.balance
    assert firm_account.take_loan(2000) is True
    assert firm_account.balance == prev_balance + 2000

def test_take_loan_no_zus():
    acc = CompanyAccount()
    acc.balance = 5000
    acc.history = [1000, -1000, 2000]
    prev_balance = acc.balance
    assert acc.take_loan(2000) is False
    assert acc.balance == prev_balance

def test_take_loan_balance_too_low(firm_account):
    firm_account.balance = 3000  # 2*2000 > 3000
    prev_balance = firm_account.balance
    assert firm_account.take_loan(2000) is False
    assert firm_account.balance == prev_balance

@pytest.mark.parametrize("bad_amount", [0, -100, "abc", None])
def test_take_loan_invalid_amount(firm_account, bad_amount):
    prev_balance = firm_account.balance
    assert firm_account.take_loan(bad_amount) is False
    assert firm_account.balance == prev_balance
