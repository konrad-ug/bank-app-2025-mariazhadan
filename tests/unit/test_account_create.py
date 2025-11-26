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
    
    def test_extract_birth_year(self):
        acc = Account("A", "B", "12345678901")
        test_data = [
            ("02222912345", 2002),
            ("99123112345", 1999),
            ("21423112345", 2121),
            ("81622912345", 2281),
            ("62010112345", 1962),
            ("12345", None),
        ]
        for pesel, expected in test_data:
            assert acc.extract_birth_year(pesel) == expected

    def test_is_eligible_for_promo(self):
        acc = Account("A", "B", "12345678901")
        assert acc.is_eligible_for_promo("70010112345") is True
        assert acc.is_eligible_for_promo("44010112345") is False
        assert acc.is_eligible_for_promo("12345") is False

    def test_receive_transfer(self):
        acc = Account("A", "B", "12345678901")
        assert acc.receive_transfer(100)
        assert acc.balance == 100.0
        assert not acc.receive_transfer(-10)
        assert not acc.receive_transfer("abc")

    def test_send_transfer(self):
        acc = Account("A", "B", "12345678901")
        acc.balance = 100
        assert acc.send_transfer(50)
        assert acc.balance == 50.0
        assert not acc.send_transfer(1000) 
        assert not acc.send_transfer(-5)
        assert not acc.send_transfer("abc")

    def test_get_express_fee(self):
        acc = Account("A", "B", "12345678901")
        assert acc.get_express_fee() == 1.0

    def test_send_express_transfer_success(self):
        acc = Account("A", "B", "12345678901")
        acc.balance = 100
        result = acc.send_express_transfer(10)
        assert result is True
        
    def test_send_express_transfer_insufficient_funds(self):
        acc = Account("A", "B", "12345678901")
        acc.balance = 5
        result = acc.send_express_transfer(10)
        assert result is False
        assert acc.balance == 5

    def test_send_express_transfer_invalid_amount(self):
        acc = Account("A", "B", "12345678901")
        assert not acc.send_express_transfer(-10)
        assert not acc.send_express_transfer("abc")
    
    def test_extract_birth_year_1800s(self):
        acc = Account("A", "B", "81921212345") 
        assert acc.extract_birth_year("81921212345") == 1881 + 0

    def test_extract_birth_year_invalid_month(self):
        acc = Account("A", "B", "00130112345")  
        assert acc.extract_birth_year("00130112345") is None

    def test_history_receive_transfer(self):
        acc = Account("A", "B", "12345678901")
        acc.receive_transfer(500)
        assert acc.history == [500.0]

    def test_history_send_transfer(self):
        acc = Account("A", "B", "12345678901")
        acc.balance = 1000
        acc.send_transfer(300)
        assert acc.history == [-300.0]

    def test_history_send_express_transfer(self):
        acc = Account("A", "B", "12345678901")
        acc.balance = 1000
        acc.send_express_transfer(300)
        assert acc.history == [-300.0, -1.0]

    def test_history_multiple_operations(self):
        acc = Account("A", "B", "12345678901")
        acc.receive_transfer(500)
        acc.send_express_transfer(300)
        assert acc.history == [500.0, -300.0, -1.0]

