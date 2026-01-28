import pytest
from src.account import Account

@pytest.fixture
def account():
    return Account("John", "Doe", "12345678901")

class TestAccount:
    def test_account_creation(self, account):
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"

    @pytest.mark.parametrize("pesel,expected", [
        ("123456789000", "Invalid"),
        ("12345", "Invalid"),
        (None, "Invalid"),
        ("12345678901", "12345678901"),
    ])
    def test_pesel_validation(self, pesel, expected):
        acc = Account("John", "Doe", pesel)
        assert acc.pesel == expected

    @pytest.mark.parametrize("promocode,expected_balance", [
        ("PROM_ABC", 50.0),
        ("PRtM_ABC", 0.0),
        ("PRM_C", 0.0),
        (4567, 0.0),
    ])
    def test_promo_codes(self, promocode, expected_balance):
        acc = Account("John", "Doe", "12345678901", promocode)
        assert acc.balance == expected_balance

    def test_promo_eligible_after_1960(self, account):
        acc = Account("John", "Doe", "70010112345", "PROM_ABC")
        assert acc.balance == 50.0

    def test_extract_birth_year(self, account):
        test_data = [
            ("02222912345", 2002),
            ("99123112345", 1999),
            ("21423112345", 2121),
            ("81622912345", 2281),
            ("62010112345", 1962),
            ("12345", None),
        ]
        for pesel, expected in test_data:
            assert account.extract_birth_year(pesel) == expected

    def test_is_eligible_for_promo(self, account):
        assert account.is_eligible_for_promo("70010112345") is True
        assert account.is_eligible_for_promo("44010112345") is False
        assert account.is_eligible_for_promo("12345") is False

    def test_receive_transfer(self, account):
        assert account.receive_transfer(100)
        assert account.balance == 100.0
        assert not account.receive_transfer(-10)
        assert not account.receive_transfer("abc")

    def test_send_transfer(self, account):
        account.balance = 100
        assert account.send_transfer(50)
        assert account.balance == 50.0
        assert not account.send_transfer(1000) 
        assert not account.send_transfer(-5)
        assert not account.send_transfer("abc")

    def test_get_express_fee(self, account):
        assert account.get_express_fee() == 1.0

    def test_send_express_transfer_success(self, account):
        account.balance = 100
        result = account.send_express_transfer(10)
        assert result is True
        
    def test_send_express_transfer_insufficient_funds(self, account):
        account.balance = 5
        result = account.send_express_transfer(10)
        assert result is False
        assert account.balance == 5

    def test_send_express_transfer_invalid_amount(self, account):
        assert not account.send_express_transfer(-10)
        assert not account.send_express_transfer("abc")
    
    def test_extract_birth_year_1800s(self, account):
        acc = Account("A", "B", "81921212345") 
        assert acc.extract_birth_year("81921212345") == 1881 + 0

    def test_extract_birth_year_invalid_month(self, account):
        acc = Account("A", "B", "00130112345")  
        assert acc.extract_birth_year("00130112345") is None
