from src.account_firm import CompanyAccount


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
