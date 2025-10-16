from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"

    def test_pesel_long(self):
        account = Account("John", "Doe", "123456789000")
        assert account.pesel == "Invalid"

    def test_pesel_short(self):
        account = Account("John", "Doe", "12345")
        assert account.pesel == "Invalid"

    def test_pesel_long(self):
        account = Account("John", "Doe", None)
        assert account.pesel == "Invalid"