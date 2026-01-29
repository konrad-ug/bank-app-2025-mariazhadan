from src.business_account import BusinessAccount
import pytest

@pytest.fixture(autouse=True)
def _stub_mf(mocker):
    return mocker.patch.object(BusinessAccount, "verify_nip_with_mf", return_value=True)

def test_ctor_raises_when_mf_denies(mocker):
    mocker.patch.object(BusinessAccount, "verify_nip_with_mf", return_value=False)
    with pytest.raises(ValueError, match="Company not registered!!"):
        BusinessAccount("TheDoors", "1234567890")

class TestBusinessAccount:

    def test_create_company_account_valid_nip(self):
        account = BusinessAccount("Tech Corp", "1234567890")
        assert account.company_name == "Tech Corp"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_create_company_account_invalid_nip_short(self):
        account = BusinessAccount("ABC Company", "123456789")
        assert account.nip == "Invalid"

    def test_create_company_account_invalid_nip_long(self):
        account = BusinessAccount("XYZ Ltd", "12345678901")
        assert account.nip == "Invalid"

    def test_create_company_account_invalid_nip_letters(self):
        account = BusinessAccount("Test Corp", "123ABC7890")
        assert account.nip == "Invalid"

    def test_company_account_receive_transfer(self):
        account = BusinessAccount("Transfer Co", "1234567890")
        result = account.receive_transfer(1000.0)
        assert result == True
        assert account.balance == 1000.0

    def test_company_account_send_transfer(self):
        account = BusinessAccount("Sender Co", "1234567890")
        account.receive_transfer(1000.0)
        result = account.send_transfer(300.0)
        assert result == True
        assert account.balance == 700.0

    def test_company_account_send_transfer_insufficient_funds(self):
        account = BusinessAccount("Poor Co", "1234567890")
        account.receive_transfer(100.0)
        result = account.send_transfer(500.0)
        assert result == False
        assert account.balance == 100.0

    def test_create_invalid_nip_letters(self):
        acc = BusinessAccount("Test Corp", "123ABC7890")
        assert acc.nip == "Invalid"

    def test_receive_transfer_positive_amount(self):
        acc = BusinessAccount("Receiver Co", "1234567890")
        assert acc.receive_transfer(500.0) is True
        assert acc.balance == 500.0

    def test_receive_transfer_negative_amount(self):
        acc = BusinessAccount("Receiver Co", "1234567890")
        assert acc.receive_transfer(-50) is False
        assert acc.balance == 0.0

    def test_receive_transfer_invalid_type(self):
        acc = BusinessAccount("Receiver Co", "1234567890")
        assert acc.receive_transfer("abc") is False
        assert acc.balance == 0.0
    
    def test_send_transfer_negative_amount(self):
        acc = BusinessAccount("Sender Co", "1234567890")
        acc.receive_transfer(100.0)
        assert acc.send_transfer(-50) is False
        assert acc.balance == 100.0
    
    def test_send_transfer_invalid_type(self):
        acc = BusinessAccount("Sender Co", "1234567890")
        acc.receive_transfer(100.0)
        assert acc.send_transfer("abc") is False
        assert acc.balance == 100.0
    
    def test_company_get_express_fee(self):
        acc = BusinessAccount("Fee Co", "1234567890")
        fee = acc.get_express_fee()
        assert fee == 5.0


@pytest.fixture
def firm_account():
    acc = BusinessAccount()
    acc.balance = 5000
    acc.history = [1000, -1775, 2000]  
    return acc

def test_take_loan_success(firm_account):
    prev_balance = firm_account.balance
    assert firm_account.take_loan(2000) is True
    assert firm_account.balance == prev_balance + 2000

def test_take_loan_no_zus():
    acc = BusinessAccount()
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
