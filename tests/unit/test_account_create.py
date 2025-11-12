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

    def test_pesel_none(self):
        account = Account("John", "Doe", None)
        assert account.pesel == "Invalid"

    def test_promo_valid(self): 
        account = Account("John", "Doe", "12345678901", "PROM_ABC")
        assert account.balance == 50.0
    
    def test_promo_invalid_prefix(self):
        account = Account("John", "Doe", "12345678901", "PRtM_ABC")
        assert account.balance == 0.0

    def test_promo_short(self):
        account = Account("John", "Doe", "12345678901", "PRM_C")
        assert account.balance == 0.0
    
    def test_promo_not_str(self):
        account = Account("John", "Doe", "12345678901", 4567)
        assert account.balance == 0.0

    def test_promo_eligible_after_1960(self):
        account = Account("John", "Doe", "70010112345", "PROM_ABC")
        assert account.balance == 50.0
    

